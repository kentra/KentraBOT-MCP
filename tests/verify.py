import asyncio
import sys
import os

# Ensure we are testing the local src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from kentrabot_mcp.server import move_logic, stop_logic, drive_logic

async def test_move():
    print("Testing move()...", end="")
    res = await move_logic(0.5, -0.5)
    assert res == "Moved: Left=0.5, Right=-0.5"
    print("OK")

async def test_stop():
    print("Testing stop()...", end="")
    res = await stop_logic()
    assert res == "STOPPED"
    print("OK")

async def test_drive():
    print("Testing drive()...", end="")
    res = await drive_logic("forward", 1.0)
    assert res == "Driving forward at speed 1.0"
    
    res = await drive_logic("left", 0.5)
    assert res == "Driving left at speed 0.5"
    print("OK")

async def main():
    await test_move()
    await test_stop()
    await test_drive()

if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("\nAll tests passed!")
    except AssertionError as e:
        print(f"\nFailed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
