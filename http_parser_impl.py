class HTTPRequest:
    def __init__(s): s.method="";s.path="";s.version="";s.headers={};s.body=""
    def __repr__(s): return f"{s.method} {s.path} {s.version} ({len(s.headers)} headers, {len(s.body)}B body)"
class HTTPResponse:
    def __init__(s): s.version="";s.status=0;s.reason="";s.headers={};s.body=""
    def __repr__(s): return f"{s.version} {s.status} {s.reason} ({len(s.headers)} headers)"
def parse_request(raw):
    req=HTTPRequest();parts=raw.split("

",1)
    header_section=parts[0];req.body=parts[1] if len(parts)>1 else ""
    lines=header_section.split("
");request_line=lines[0].split(" ",2)
    req.method=request_line[0];req.path=request_line[1] if len(request_line)>1 else "/"
    req.version=request_line[2] if len(request_line)>2 else "HTTP/1.1"
    for line in lines[1:]:
        if ": " in line: k,v=line.split(": ",1);req.headers[k.lower()]=v
    return req
def parse_response(raw):
    res=HTTPResponse();parts=raw.split("

",1)
    header_section=parts[0];res.body=parts[1] if len(parts)>1 else ""
    lines=header_section.split("
");status_line=lines[0].split(" ",2)
    res.version=status_line[0];res.status=int(status_line[1]) if len(status_line)>1 else 0
    res.reason=status_line[2] if len(status_line)>2 else ""
    for line in lines[1:]:
        if ": " in line: k,v=line.split(": ",1);res.headers[k.lower()]=v
    return res
def build_request(method,path,headers=None,body=""):
    h=headers or {};lines=[f"{method} {path} HTTP/1.1"]
    for k,v in h.items(): lines.append(f"{k}: {v}")
    if body: lines.append(f"Content-Length: {len(body)}")
    return "
".join(lines)+"

"+body
def demo():
    raw="GET /api/users HTTP/1.1
Host: example.com
Accept: application/json

"
    req=parse_request(raw);print(f"Request: {req}");print(f"  Host: {req.headers.get('host')}")
    raw_res="HTTP/1.1 200 OK
Content-Type: text/html

<h1>Hello</h1>"
    res=parse_response(raw_res);print(f"Response: {res}");print(f"  Body: {res.body}")
    built=build_request("POST","/api/data",{"Host":"api.example.com"},'{"key":"value"}')
    print(f"Built: {parse_request(built)}")
if __name__ == "__main__": demo()
