from bs4 import BeautifulSoup
import requests, json, re, time
import pickle as pkl


url_list = [
"https://www.paytmmoney.com/mutual-funds/scheme/nippon-india-pharma-fund-direct-growth/inf204k01i50",
"https://www.paytmmoney.com/mutual-funds/scheme/icici-prudential-technology-direct-plan-growth/inf109k01z48",
"https://www.paytmmoney.com/mutual-funds/scheme/tata-india-pharma-healthcare-fund-direct-growth/inf277k019a3",
"https://www.paytmmoney.com/mutual-funds/scheme/aditya-birla-sun-life-digital-india-fund-direct-growth/inf209k01vf2",
"https://www.paytmmoney.com/mutual-funds/scheme/quant-small-cap-fund-direct-plan-growth/inf966l01689",
"https://www.paytmmoney.com/mutual-funds/scheme/uti-healthcare-fund-direct-growth/inf789f01to9",
"https://www.paytmmoney.com/mutual-funds/scheme/sbi-healthcare-opportunities-fund-direct-plan-growth/inf200k01up2",
"https://www.paytmmoney.com/mutual-funds/scheme/dhfl-pramerica-global-equity-opportunities-fund-direct-growth/inf223j01nf2",
"https://www.paytmmoney.com/mutual-funds/scheme/tata-digital-india-fund-direct-growth/inf277k01z77",
"https://www.paytmmoney.com/mutual-funds/scheme/quant-active-fund-direct-growth/inf966l01614",
"https://www.paytmmoney.com/mutual-funds/scheme/icici-prudential-commodities-fund-direct-growth/inf109kc1f91",
"https://www.paytmmoney.com/mutual-funds/scheme/quant-mid-cap-fund-direct-growth/inf966l01887",
"https://www.paytmmoney.com/mutual-funds/scheme/quant-infrastructure-fund-direct-growth/inf966l01721",
"https://www.paytmmoney.com/mutual-funds/scheme/sbi-magnum-comma-fund-direct-growth/inf200k01sb6",
"https://www.paytmmoney.com/mutual-funds/scheme/quant-consumption-fund-direct-growth/inf966l01911",
"https://www.paytmmoney.com/mutual-funds/scheme/dsp-natural-resources-and-new-energy-fund-direct-plan-growth/inf740k01qa7",
"https://www.paytmmoney.com/mutual-funds/scheme/tata-small-cap-fund-direct-growth/inf277k011o1",
"https://www.paytmmoney.com/mutual-funds/scheme/lnt-emerging-businesses-fund-direct-growth/inf917k01qa1",
"https://www.paytmmoney.com/mutual-funds/scheme/nippon-india-banking-fund-direct-growth/inf204k01xo1",
"https://www.paytmmoney.com/mutual-funds/scheme/aditya-birla-sun-life-psu-equity-fund-direct-growth/inf209kb1o82",
"https://www.paytmmoney.com/mutual-funds/scheme/icici-prudential-banking-and-financial-services-direct-plan-growth/inf109k013j1",
"https://www.paytmmoney.com/mutual-funds/scheme/sbi-psu-direct-plan-growth/inf200k01uy4",
"https://www.paytmmoney.com/mutual-funds/scheme/canara-robeco-small-cap-fund-direct-growth/inf760k01jc6",
"https://www.paytmmoney.com/mutual-funds/scheme/principal-small-cap-fund-direct-growth/inf173k01ok5"
]

main_dict = {}

for idx in range(10000, len(url_list)):
    url = url_list[idx]
    # Initialization
    fund_name = url.split('/')[5]
    main_dict[fund_name] = {'rank': idx}
    print(f"fetching {fund_name}")
    fetched = False
    # Pinging
    while not fetched:
        try:
            r = requests.get(url)
            fetched = True
            print(f"success\n")
        except Exception as e:
            print(f"{e}, retrying...")
            # Retrying after 10 second delay
            time.sleep(10)
    soup = BeautifulSoup(r.content, 'html5lib')
    # Parsing HTML
    key_string = "__NEXT_DATA__ = "
    end_char = ";"
    text_data = soup.find('script', text=re.compile(key_string)).text
    text_data = text_data[len(key_string):text_data.index(end_char)]
    # Converting text to dict
    info_dict = json.loads(text_data)
    # Extracting relevant info
    sectors_dict = info_dict['props']['pageProps']['initialMfData']['sections'][0]
    companies_dict = info_dict['props']['pageProps']['initialMfData']['sections'][1]
    main_dict[fund_name]['sectors'] = sectors_dict
    main_dict[fund_name]['companies'] = companies_dict

    with open('data/extracted_dict.pkl', 'wb') as f:
        pkl.dump(main_dict, f)
        f.close()
