# How to use MCP safely

An MCP server can expose tools, files, accounts, and services to an AI application. Install servers only from sources you trust, inspect configuration examples, pin versions where practical, and grant the narrowest credentials and filesystem access possible.

Keep secrets in the client's supported secret store or environment configuration—never in committed JSON. Test destructive tools against disposable data, confirm tool calls when the client supports approval controls, and rotate credentials after suspected exposure.

See the [official MCP documentation](https://modelcontextprotocol.io/) for protocol and client concepts.
