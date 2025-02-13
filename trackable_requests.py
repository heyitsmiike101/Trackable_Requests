import requests
import json
from datetime import datetime
import time


class trackable_request:
    def __init__(self, headers: dict = None) -> None:
        self._headers = headers
        self.request_list = []

    @property
    def headers(self) -> dict:
        if not self._headers:
            raise ValueError("Headers must be set before making a request.")
        return self._headers

    @headers.setter
    def headers(self, headers: dict) -> None:
        if headers is None:
            raise ValueError("Headers cannot be set to None.")
        self._headers = headers

    def _make_request(
        self,
        method: str,
        url: str,
        params: dict = None,
        data: dict = None,
        json: dict = None,
    ):
        """Handles request execution while tracking response time and timestamp."""
        start_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )  # Timestamp for request sent
        start_perf = time.perf_counter()  # Start timing

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                data=data,
                json=json,
            )
            response.raise_for_status()
            response_time = round(
                (time.perf_counter() - start_perf) * 1000, 2
            )  # Convert to milliseconds
            return response.json(), None, start_time, response_time
        except requests.exceptions.RequestException as e:
            response_time = round(
                (time.perf_counter() - start_perf) * 1000, 2
            )  # Capture failure response time
            return None, str(e), start_time, response_time

    def _log_request(
        self,
        method: str,
        url: str,
        params,
        data,
        json,
        response,
        error,
        start_time,
        response_time,
    ):
        """Handles logging request details with timestamps and response times."""
        self.request_list.append(
            {
                "method": method,
                "url": url,
                "params": params,
                "data": data,
                "json": json,
                "response": response,
                "error": error,
                "request_sent": start_time,  # When request was sent
                "response_time_ms": response_time,  # Response time in milliseconds
            }
        )

    def get(self, url: str, params: dict = None) -> dict:
        response, error, start_time, response_time = self._make_request(
            "GET", url, params=params
        )
        self._log_request(
            "GET", url, params, None, None, response, error, start_time, response_time
        )
        return response

    def post(self, url: str, data: dict = None, json: dict = None) -> dict:
        response, error, start_time, response_time = self._make_request(
            "POST", url, None, data, json
        )
        self._log_request(
            "POST", url, None, data, json, response, error, start_time, response_time
        )
        return response

    def put(self, url: str, data: dict = None, json: dict = None) -> dict:
        response, error, start_time, response_time = self._make_request(
            "PUT", url, None, data, json
        )
        self._log_request(
            "PUT", url, None, data, json, response, error, start_time, response_time
        )
        return response

    def patch(self, url: str, data: dict = None, json: dict = None) -> dict:
        response, error, start_time, response_time = self._make_request(
            "PATCH", url, None, data, json
        )
        self._log_request(
            "PATCH", url, None, data, json, response, error, start_time, response_time
        )
        return response

    def delete(self, url: str, params: dict = None) -> dict:
        response, error, start_time, response_time = self._make_request(
            "DELETE", url, params=params
        )
        self._log_request(
            "DELETE",
            url,
            params,
            None,
            None,
            response,
            error,
            start_time,
            response_time,
        )
        return response

    # def _generate_request_html(self):
    #     """Generates HTML content for each request entry with syntax highlighting."""
    #     html_content = ""
    #     for req in self.request_list:
    #         request_info = json.dumps(
    #             {
    #                 "method": req["method"],
    #                 "url": req["url"],
    #                 "params": req["params"],
    #                 "data": req["data"],
    #                 "json": req["json"],
    #             },
    #             indent=4,
    #         )

    #         response_info = (
    #             json.dumps(req["response"], indent=4)
    #             if req["response"]
    #             else "No Response"
    #         )
    #         error_info = req["error"]

    #         request_sent = req["request_sent"]
    #         response_time = req["response_time_ms"]

    #         html_content += f"""
    #         <div class="request-box">
    #             <details>
    #                 <summary>{req["method"]} - {req["url"]} <span style="float:right;">⏳ {response_time} ms</span></summary>
    #                 <p><strong>Sent:</strong> {request_sent}</p>
    #                 <details>
    #                     <summary>Request Info</summary>
    #                     <pre><code class="json">{request_info}</code></pre>
    #                 </details>
    #                 <details>
    #                     <summary>Response</summary>
    #                     <pre><code class="json">{response_info}</code></pre>
    #                 </details>
    #                 {f'<details><summary>Error</summary><pre class="error"><code>{error_info}</code></pre></details>' if error_info else ""}
    #             </details>
    #         </div>
    #         """
    #     return html_content

    # def export_html(
    #     self, filename="request_log.html", redact_authorization_header=True
    # ):
    #     """Exports the request list to a dark-themed HTML file with dropdowns, timeline, and properly formatted JSON (no syntax highlighting)."""
    #     report_date = datetime.now().strftime(
    #         "%Y-%m-%d %H:%M:%S"
    #     )  # Get current timestamp

    #     # Redact Authorization if True.
    #     if redact_authorization_header:
    #         print_headers = (
    #             self.headers.copy()
    #         )  # Ensure we don't modify the original headers
    #         print_headers["Authorization"] = "REDACTED"
    #     else:
    #         print_headers = self.headers

    #     html_template = f"""
    #     <!DOCTYPE html>
    #     <html lang="en">
    #     <head>
    #         <meta charset="UTF-8">
    #         <meta name="viewport" content="width=device-width, initial-scale=1.0">
    #         <title>Request Log</title>
    #         <style>
    #             body {{
    #                 font-family: Arial, sans-serif;
    #                 background-color: #36393f;
    #                 color: #dcddde;
    #                 padding: 20px;
    #             }}
    #             .container {{
    #                 width: 80%;
    #                 margin: auto;
    #             }}
    #             .header-box {{
    #                 background: #2f3136;
    #                 border-radius: 5px;
    #                 padding: 15px;
    #                 margin-bottom: 20px;
    #                 box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    #             }}
    #             .timeline {{
    #                 position: relative;
    #                 margin-left: 20px;
    #             }}
    #             .timeline::before {{
    #                 content: "";
    #                 position: absolute;
    #                 left: 10px;
    #                 top: 0;
    #                 width: 4px;
    #                 height: 100%;
    #                 background: #7289da; /* Discord blue */
    #             }}
    #             .request-box {{
    #                 position: relative;
    #                 background: #2f3136;
    #                 border-radius: 5px;
    #                 padding: 15px;
    #                 margin-bottom: 15px;
    #                 box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
    #                 border-left: 5px solid #7289da;
    #             }}
    #             .request-box::before {{
    #                 content: "";
    #                 position: absolute;
    #                 left: -14px;
    #                 top: 20px;
    #                 width: 12px;
    #                 height: 12px;
    #                 background: #7289da;
    #                 border-radius: 50%;
    #                 border: 3px solid #2f3136;
    #             }}
    #             summary {{
    #                 font-size: 16px;
    #                 font-weight: bold;
    #                 cursor: pointer;
    #                 padding: 5px;
    #             }}
    #             pre {{
    #                 background: #202225;
    #                 padding: 10px;
    #                 border-radius: 5px;
    #                 overflow-x: auto;
    #                 white-space: pre-wrap;
    #                 word-wrap: break-word;
    #                 color: #99ff99; /* Light green */
    #             }}
    #             .error {{
    #                 color: #ff6b6b;
    #             }}
    #             code {{
    #                 font-size: 14px;
    #                 font-family: "Courier New", monospace;
    #             }}
    #         </style>
    #     </head>
    #     <body>
    #         <div class="container">
    #             <h2>Request Log</h2>
    #             <p><strong>Generated on:</strong> {report_date}</p>
    #             <p><strong>Total Requests:</strong> {len(self.request_list)}</p>
    #             <div class="header-box">
    #                 <h3>Headers</h3>
    #                 <pre>{json.dumps(print_headers, indent=4)}</pre>
    #             </div>
    #             <div class="timeline">
    #                 {self._generate_request_html()}
    #             </div>
    #         </div>
    #     </body>
    #     </html>
    #     """

    #     with open(filename, "w", encoding="utf-8") as f:
    #         f.write(html_template)
    #     print(f"Request log exported to {filename}")

    def export_html(
        self, filename="request_log.html", redact_authorization_header=True
    ):
        """Exports the request list to a dark-themed HTML file with headers and requests sharing the same width."""
        report_date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )  # Get current timestamp

        # Redact Authorization if True.
        if redact_authorization_header:
            print_headers = (
                self.headers.copy()
            )  # Ensure we don't modify the original headers
            print_headers["Authorization"] = "REDACTED"
        else:
            print_headers = self.headers

        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Request Log</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #36393f;
                    color: #dcddde;
                    padding: 20px;
                }}
                .container {{
                    max-width: 90%;
                    margin: auto;
                }}

                /* HEADER & REQUEST SECTIONS */
                .section-box {{
                    background: #2f3136;
                    border-radius: 8px;
                    padding: 20px;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
                    border-left: 6px solid #7289da;
                    width: 95%;
                    margin: 20px auto;
                }}
                .section-box h3 {{
                    font-size: 20px;
                    margin-bottom: 10px;
                }}
                .section-box pre {{
                    background: #202225;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                    color: #99ff99; /* Light green */
                    font-size: 14px;
                }}

                /* TIMELINE */
                .timeline {{
                    position: relative;
                    max-width: 100%;
                    margin: auto;
                    padding: 10px 0;
                }}
                .timeline::before {{
                    content: '';
                    position: absolute;
                    width: 6px;
                    background-color: #7289da;
                    top: 0;
                    bottom: 0;
                    left: 25px;
                    margin-left: -3px;
                }}
                .timeline-entry {{
                    position: relative;
                    padding: 20px 40px;
                    box-sizing: border-box;
                    margin-bottom: 20px;
                    display: flex;
                    align-items: center;
                    width: 95%;
                    margin-left: auto;
                    margin-right: auto;
                }}
                .timeline-marker {{
                    position: absolute;
                    left: 10px;
                    width: 20px;
                    height: 20px;
                    background-color: #7289da;
                    border-radius: 50%;
                    border: 3px solid #2f3136;
                }}
                .timeline-card {{
                    background: #2f3136;
                    border-radius: 8px;
                    padding: 20px;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
                    border-left: 6px solid #7289da;
                    width: 100%;
                }}

                summary {{
                    font-size: 18px;
                    font-weight: bold;
                    cursor: pointer;
                    padding: 8px;
                }}
                pre {{
                    background: #202225;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                    color: #99ff99; /* Light green */
                }}
                .error {{
                    color: #ff6b6b;
                }}
                code {{
                    font-size: 16px;
                    font-family: "Courier New", monospace;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Request Log</h2>
                <p><strong>Generated on:</strong> {report_date}</p>
                <p><strong>Total Requests:</strong> {len(self.request_list)}</p>

                <!-- Headers Section -->
                <div class="section-box">
                    <h3>Headers</h3>
                    <pre>{json.dumps(print_headers, indent=4)}</pre>
                </div>

                <!-- Requests Section -->
                <div class="timeline">
                    {self._generate_request_html()}
                </div>
            </div>
        </body>
        </html>
        """

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_template)
        print(f"Request log exported to {filename}")

    def _generate_request_html(self):
        """Generates HTML content for each request entry, ensuring full-width consistency."""
        html_content = ""
        for req in self.request_list:
            request_info = json.dumps(
                {
                    "method": req["method"],
                    "url": req["url"],
                    "params": req["params"],
                    "data": req["data"],
                    "json": req["json"],
                },
                indent=4,
            )

            response_info = (
                json.dumps(req["response"], indent=4)
                if req["response"]
                else "No Response"
            )
            error_info = req["error"]

            request_sent = req["request_sent"]
            response_time = req["response_time_ms"]

            html_content += f"""
            <div class="timeline-entry">
                <div class="timeline-marker"></div>
                <div class="timeline-card">
                    <details>
                        <summary>{req["method"]} - {req["url"]} <span style="float:right;">⏳ {response_time} ms</span></summary>
                        <p><strong>Sent:</strong> {request_sent}</p>
                        <details>
                            <summary>Request Info</summary>
                            <pre>{request_info}</pre>
                        </details>
                        <details>
                            <summary>Response</summary>
                            <pre>{response_info}</pre>
                        </details>
                        {f'<details><summary>Error</summary><pre class="error">{error_info}</pre></details>' if error_info else ""}
                    </details>
                </div>
            </div>
            """
        return html_content
