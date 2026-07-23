import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pyback.core.server import Server, Request, Response
from pyback.core.config import Settings
from pyback.core.logging import configure_logging
from pyback.middleware.base import LoggerMiddleware
from pyback.api.bridge import expose, rpc_handler
from fares_db import lookup_fare, fuzzy_lookup


@expose
def get_fare(res, postcode_prefix: str):
    result = lookup_fare(postcode_prefix)
    if not result:
        result = fuzzy_lookup(postcode_prefix)
    return result


@expose
def all_fares(res):
    from fares_db import get_conn
    with get_conn() as conn:
        cursor = conn.execute("SELECT postcode_prefix, cost, zone FROM fares ORDER BY postcode_prefix")
        rows = cursor.fetchall()
        return [{"prefix": r[0], "cost": r[1], "zone": r[2]} for r in rows]


class FareCabServer(Server):
    def __init__(self, port: int = 8080, directory: str = "."):
        super().__init__(port=port)
        self.directory = directory
        self._add_routes()

    def _add_routes(self):
        self.route("/api/rpc", method="POST")(rpc_handler)

    def _chain(self, req: Request, res: Response):
        match = self.router.resolve(req.method, req.path)
        if match:
            handler_func, params = match
            req.params = params
            handler_func(req, res)
            return

        if req.method == "GET":
            self._serve_static(req, res)
        else:
            res.status = 405
            res.text_body("Method Not Allowed")

    def _serve_static(self, req: Request, res: Response):
        path = req.path.split("?")[0]
        if path == "/":
            path = "/index.html"
        file_path = os.path.join(self.directory, path.lstrip("/"))
        file_path = os.path.normpath(file_path)

        if not file_path.startswith(os.path.normpath(self.directory)):
            res.status = 403
            res.text_body("Forbidden")
            return

        if os.path.isfile(file_path):
            ext = os.path.splitext(file_path)[1]
            mime_map = {
                ".html": "text/html",
                ".css": "text/css",
                ".js": "application/javascript",
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".svg": "image/svg+xml",
                ".json": "application/json",
                ".ico": "image/x-icon",
            }
            res.headers["Content-Type"] = mime_map.get(ext, "application/octet-stream")
            with open(file_path, "rb") as f:
                res.body = f.read().decode("utf-8")
            res.status = 200
        else:
            res.status = 404
            res.text_body("Not Found")


if __name__ == "__main__":
    configure_logging("INFO")
    settings = Settings.from_env()
    server_dir = os.path.dirname(os.path.abspath(__file__))
    server = FareCabServer(port=settings.port, directory=server_dir)
    server.use(LoggerMiddleware)
    print(f"Fare-Cab server running at http://localhost:{settings.port}")
    server.run()
