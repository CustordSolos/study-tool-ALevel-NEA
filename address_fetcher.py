import requests

"""
Verifies and retrieves addresses
"""


class AddressSearch:
    api_url = "https://geocode.search.hereapi.com/v1/geocode"
    api_key = ""

    @staticmethod
    def get_address_details(house_number: int, postal_code: str) -> dict:
        """
        Fetches address details using the HERE Geocoding API.

        Returns:
            Dict[str, dict]: Dictionary containg an error (if address is invalid or and HTTPError is raised) and address if found.
        """
        result = {"result": False, "err_msg": "", "address": {}}
        query_params = {
            "qq": f"houseNumber={house_number};postalCode={postal_code}",
            "apiKey": AddressSearch.api_key,
        }
        try:
            response = requests.get(AddressSearch.api_url, params=query_params)
            # Raise an HTTPError for bad responses
            response.raise_for_status()
            data = response.json()
            if data.get("items"):
                for item in data["items"]:
                    if not item["address"]:
                        result["err_msg"] = "Failed to retrieve a full address."
                        return result
                    address = item["address"]
                    result["address"] = {
                        "postcode": postal_code.upper().replace(" ", ""),
                        "city": address.get("city"),
                        "country": address.get("countryName"),
                        "house_number": house_number,
                        "label": address.get("label"),
                    }
                    result["result"] = True
                    return result
            else:
                result["err_msg"] = "No address found."
                return result
        except requests.exceptions.RequestException as e:
            result["err_msg"] = f"An error occurred: {e}"
            return result
