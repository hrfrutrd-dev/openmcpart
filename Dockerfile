FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml README.md ./
COPY src/ ./src/
RUN pip install --no-cache-dir -e .

# MCP server runs via stdio, so no port exposure needed
# But for SSE transport future, expose 8000
EXPOSE 8000

# Default command
CMD ["openmcpart"]

# For MCP Inspector testing:
# docker run -i --rm openmcpart-design
# Or with SSE:
# docker run -p 8000:8000 -e MCP_TRANSPORT=sse openmcpart-design
