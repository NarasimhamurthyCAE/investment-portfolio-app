from core.metadata.services.metadata_service import MetadataService


def main():

    service = MetadataService()

    metadata = service.refresh(

        symbol="INFY.NS",

        asset_type="STOCK",

    )

    print("=" * 80)

    print(metadata)

    print("=" * 80)

    print("Company :", metadata.company_name)
    print("Sector  :", metadata.sector)
    print("Industry:", metadata.industry)
    print("Exchange:", metadata.exchange)
    print("Country :", metadata.country)

    print("=" * 80)


if __name__ == "__main__":

    main()