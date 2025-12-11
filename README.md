# KentraBOT MCP Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server for controlling a two-track robot. This server exposes tools to control motor speeds and direction, allowing LLMs to drive the robot.

## Features

-   **Movement Control**: Independent control of left and right tracks.
-   **High-Level Commands**: `drive` tool for easy direction control (forward, backward, left, right).
-   **Safety**: Emergency `stop` tool.
-   **Hardware Abstraction**: Built with a modular driver system. Currently configured with a `Dummy` driver for simulation/testing.

## Installation

### Prerequisites
-   Python 3.11 or higher
-   `uv` (recommended) or `pip`

### Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd kentraBOT-MCP
    ```

2.  **Install dependencies**:
    Using `uv`:
    ```bash
    uv sync
    ```
    
    Or using standard `pip`:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install .
    ```

## Usage

### Running the Server

Start the MCP server using `uv`:

```bash
uv run kentrabot
```

Or directly with python:

```bash
python3 src/kentrabot_mcp/server.py
```

### connecting to an MCP Client

Configure your MCP client (e.g., Claude Desktop, MCP Inspector) to run the server command above.

**Example `claude_desktop_config.json`**:
```json
{
  "mcpServers": {
    "kentrabot": {
      "command": "uv",
      "args": ["run", "kentrabot"]
    }
  }
}
```

## Tools

| Tool | Description | Arguments |
|------|-------------|-----------|
| `move` | Set independent track speeds | `left_speed` (-1.0 to 1.0), `right_speed` (-1.0 to 1.0) |
| `drive` | Move in a specific direction | `direction` (forward, backward, left, right), `speed` (0.0 to 1.0) |
| `stop` | Stop both motors | None |

## Hardware Configuration

Currently, the server is set to use the `DummyRobot` driver which logs actions to the console. 

To use real hardware (e.g., Raspberry Pi with Motor Hat):
1.  Implement a new driver in `src/kentrabot_mcp/drivers/`.
2.  Inherit from `kentrabot_mcp.robot.Robot`.
3.  Update `src/kentrabot_mcp/server.py` to initialize your new driver.
