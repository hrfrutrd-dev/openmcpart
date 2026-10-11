FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml README.md ./
COPY src/ ./src/
RUN pip install --no-cache-dir -e .

# HTTP is opt-in. In containers, bind broadly so an explicitly published port is reachable.
ENV MCP_HOST=0.0.0.0
EXPOSE 8000

# Default command
CMD ["openmcpart"]

# For MCP Inspector testing:
# docker run -i --rm openmcpart-design
# For HTTP transports:
# docker run -p 8000:8000 -e MCP_TRANSPORT=streamable-http openmcpart-design
# Or use MCP_TRANSPORT=sse
