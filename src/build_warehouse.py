from src.extract import extract_all


def main() -> None:
    extract_all()
    print("Raw extraction complete. Transform and warehouse build are next steps.")


if __name__ == "__main__":
    main()