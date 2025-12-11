import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from kentrabot_mcp.server import move_logic, stop_logic, drive_logic

def test_move():
    print("Testing move()...", end="")
    res = move_logic(0.5, -0.5)
    assert res == "Moved: Left=0.5, Right=-0.5"
    print("OK")

def test_stop():
    print("Testing stop()...", end="")
    res = stop_logic()
    assert res == "STOPPED"
    print("OK")

def test_drive():
    print("Testing drive()...", end="")
    res = drive_logic("forward", 1.0)
    assert res == "Driving forward at speed 1.0"
    
    res = drive_logic("left", 0.5)
    assert res == "Driving left at speed 0.5"
    print("OK")

if __name__ == "__main__":
    try:
        test_move()
        test_stop()
        test_drive()
        print("\nAll tests passed!")
    except AssertionError as e:
        print(f"\nFailed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
