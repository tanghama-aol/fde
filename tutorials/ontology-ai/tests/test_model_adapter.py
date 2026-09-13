import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

from ontology_lab.common import DATA, NORTH_PLANNER, LabError, read_json
from ontology_lab.generation import SCHEMA, ollama_recommendation
from ontology_lab.retrieval import Retriever


class ModelAdapterTests(unittest.TestCase):
    def setUp(self):
        self.requests = []
        self.status = 200
        self.body = {"model":"protocol-test-double","done":True,"response":json.dumps(read_json(DATA/"recommendation.fixture.json"))}
        owner = self
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                owner.requests.append({"path":self.path,"body":json.loads(self.rfile.read(int(self.headers["Content-Length"])))})
                raw = json.dumps(owner.body).encode()
                self.send_response(owner.status)
                self.send_header("Content-Type","application/json")
                self.send_header("Content-Length",str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
            def log_message(self, *args): pass
        self.server = HTTPServer(("127.0.0.1",0),Handler)
        self.thread = threading.Thread(target=self.server.serve_forever,daemon=True)
        self.thread.start()
        self.url = "http://127.0.0.1:"+str(self.server.server_port)
        self.bundle = Retriever().bundle(NORTH_PLANNER,"P-101","P-101")

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def test_protocol_and_validation_using_local_http_double(self):
        result,run = ollama_recommendation(self.bundle,"test-model",base_url=self.url,timeout=2)
        self.assertEqual(self.requests[0]["path"],"/api/generate")
        self.assertEqual(self.requests[0]["body"]["format"],SCHEMA)
        self.assertFalse(self.requests[0]["body"]["stream"])
        self.assertEqual(result["temperature_c"],92)
        self.assertFalse(run["executed_business_action"])

    def test_incomplete_and_invalid_model_response(self):
        self.body["done"] = False
        with self.assertRaises(LabError) as caught: ollama_recommendation(self.bundle,"test",base_url=self.url,timeout=2)
        self.assertEqual(caught.exception.code,"MODEL_RESPONSE")
        self.body = {"done":True,"response":"not-json"}
        with self.assertRaises(LabError): ollama_recommendation(self.bundle,"test",base_url=self.url,timeout=2)
        self.body = []
        with self.assertRaises(LabError): ollama_recommendation(self.bundle,"test",base_url=self.url,timeout=2)

    def test_http_failure_is_not_retried_as_action(self):
        self.status = 503
        with self.assertRaises(LabError) as caught: ollama_recommendation(self.bundle,"test",base_url=self.url,timeout=2)
        self.assertEqual(caught.exception.code,"MODEL_UNAVAILABLE")
        self.assertEqual(len(self.requests),1)

    def test_remote_endpoint_needs_explicit_operator_selection(self):
        with self.assertRaises(LabError) as caught: ollama_recommendation(self.bundle,"test",base_url="https://example.org")
        self.assertEqual(caught.exception.code,"REMOTE_ENDPOINT")
        self.assertEqual(self.requests,[])


if __name__ == "__main__": unittest.main()
