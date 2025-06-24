import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="piper",
    )
    parser.add_argument("-v", "--version", action="version", version="0.1.0")
    parser.parse_args()

    print("Hello from PiPER!")


if __name__ == "__main__":
    main()
