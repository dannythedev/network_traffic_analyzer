import requests
import json


class IPReputationClient:
    COUNTRY_CODES = {
        'AD': 'Andorra',
        'AE': 'UAE',
        'AF': 'Afghanistan',
        'AG': 'Antigua',
        'AI': 'Anguilla',
        'AL': 'Albania',
        'AM': 'Armenia',
        'AO': 'Angola',
        'AQ': 'Antarctica',
        'AR': 'Argentina',
        'AS': 'Samoa',
        'AT': 'Austria',
        'AU': 'Australia',
        'AW': 'Aruba',
        'AX': 'Åland',
        'AZ': 'Azerbaijan',
        'BA': 'Bosnia',
        'BB': 'Barbados',
        'BD': 'Bangladesh',
        'BE': 'Belgium',
        'BF': 'Burkina Faso',
        'BG': 'Bulgaria',
        'BH': 'Bahrain',
        'BI': 'Burundi',
        'BJ': 'Benin',
        'BL': 'Saint Barts',
        'BM': 'Bermuda',
        'BN': 'Brunei',
        'BO': 'Bolivia',
        'BQ': 'Bonaire',
        'BR': 'Brazil',
        'BS': 'Bahamas',
        'BT': 'Bhutan',
        'BV': 'Bouvet Island',
        'BW': 'Botswana',
        'BY': 'Belarus',
        'BZ': 'Belize',
        'CA': 'Canada',
        'CC': 'Cocos',
        'CD': 'Congo (DRC)',
        'CF': 'CAR',
        'CG': 'Congo',
        'CH': 'Switzerland',
        'CI': 'Côte d\'Ivoire',
        'CK': 'Cook Islands',
        'CL': 'Chile',
        'CM': 'Cameroon',
        'CN': 'China',
        'CO': 'Colombia',
        'CR': 'Costa Rica',
        'CU': 'Cuba',
        'CV': 'Cabo Verde',
        'CW': 'Curaçao',
        'CX': 'Christmas Island',
        'CY': 'Cyprus',
        'CZ': 'Czechia',
        'DE': 'Germany',
        'DJ': 'Djibouti',
        'DK': 'Denmark',
        'DM': 'Dominica',
        'DO': 'Dominican Rep.',
        'DZ': 'Algeria',
        'EC': 'Ecuador',
        'EE': 'Estonia',
        'EG': 'Egypt',
        'EH': 'W. Sahara',
        'ER': 'Eritrea',
        'ES': 'Spain',
        'ET': 'Ethiopia',
        'FI': 'Finland',
        'FJ': 'Fiji',
        'FM': 'Micronesia',
        'FO': 'Faroe Islands',
        'FR': 'France',
        'GA': 'Gabon',
        'GB': 'United Kingdom',
        'GD': 'Grenada',
        'GE': 'Georgia',
        'GF': 'French Guiana',
        'GG': 'Guernsey',
        'GH': 'Ghana',
        'GI': 'Gibraltar',
        'GL': 'Greenland',
        'GM': 'Gambia',
        'GN': 'Guinea',
        'GP': 'Guadeloupe',
        'GQ': 'Eq. Guinea',
        'GR': 'Greece',
        'GS': 'S. Georgia',
        'GT': 'Guatemala',
        'GU': 'Guam',
        'GW': 'Guinea-Bissau',
        'GY': 'Guyana',
        'HK': 'Hong Kong',
        'HM': 'Heard Island',
        'HN': 'Honduras',
        'HR': 'Croatia',
        'HT': 'Haiti',
        'HU': 'Hungary',
        'ID': 'Indonesia',
        'IE': 'Ireland',
        'IL': 'Israel',
        'IM': 'Isle of Man',
        'IN': 'India',
        'IO': 'B.I.O.T.',
        'IQ': 'Iraq',
        'IR': 'Iran',
        'IS': 'Iceland',
        'IT': 'Italy',
        'JE': 'Jersey',
        'JM': 'Jamaica',
        'JO': 'Jordan',
        'JP': 'Japan',
        'KE': 'Kenya',
        'KG': 'Kyrgyzstan',
        'KH': 'Cambodia',
        'KI': 'Kiribati',
        'KM': 'Comoros',
        'KN': 'St. Kitts',
        'KP': 'North Korea',
        'KR': 'South Korea',
        'KW': 'Kuwait',
        'KY': 'Cayman Islands',
        'KZ': 'Kazakhstan',
        'LA': 'Laos',
        'LB': 'Lebanon',
        'LC': 'St. Lucia',
        'LI': 'Liechtenstein',
        'LK': 'Sri Lanka',
        'LR': 'Liberia',
        'LS': 'Lesotho',
        'LT': 'Lithuania',
        'LU': 'Luxembourg',
        'LV': 'Latvia',
        'LY': 'Libya',
        'MA': 'Morocco',
        'MC': 'Monaco',
        'MD': 'Moldova',
        'ME': 'Montenegro',
        'MF': 'St. Martin',
        'MG': 'Madagascar',
        'MH': 'Marshall Is.',
        'MK': 'North Macedonia',
        'ML': 'Mali',
        'MM': 'Myanmar',
        'MN': 'Mongolia',
        'MO': 'Macau',
        'MP': 'N. Mariana Is.',
        'MQ': 'Martinique',
        'MR': 'Mauritania',
        'MS': 'Montserrat',
        'MT': 'Malta',
        'MU': 'Mauritius',
        'MV': 'Maldives',
        'MW': 'Malawi',
        'MX': 'Mexico',
        'MY': 'Malaysia',
        'MZ': 'Mozambique',
        'NA': 'Namibia',
        'NC': 'New Caledonia',
        'NE': 'Niger',
        'NF': 'Norfolk Island',
        'NG': 'Nigeria',
        'NI': 'Nicaragua',
        'NL': 'Netherlands',
        'NO': 'Norway',
        'NP': 'Nepal',
        'NR': 'Nauru',
        'NU': 'Niue',
        'NZ': 'New Zealand',
        'OM': 'Oman',
        'PA': 'Panama',
        'PE': 'Peru',
        'PF': 'French Polynesia',
        'PG': 'Papua N.G.',
        'PH': 'Philippines',
        'PK': 'Pakistan',
        'PL': 'Poland',
        'PM': 'St. Pierre',
        'PN': 'Pitcairn',
        'PR': 'Puerto Rico',
        'PS': 'Palestine',
        'PT': 'Portugal',
        'PW': 'Palau',
        'PY': 'Paraguay',
        'QA': 'Qatar',
        'RE': 'Réunion',
        'RO': 'Romania',
        'RS': 'Serbia',
        'RU': 'Russia',
        'RW': 'Rwanda',
        'SA': 'Saudi Arabia',
        'SB': 'Solomon Is.',
        'SC': 'Seychelles',
        'SD': 'Sudan',
        'SE': 'Sweden',
        'SG': 'Singapore',
        'SH': 'St. Helena',
        'SI': 'Slovenia',
        'SJ': 'Svalbard',
        'SK': 'Slovakia',
        'SL': 'Sierra Leone',
        'SM': 'San Marino',
        'SN': 'Senegal',
        'SO': 'Somalia',
        'SR': 'Suriname',
        'SS': 'S. Sudan',
        'ST': 'São Tomé',
        'SV': 'El Salvador',
        'SX': 'Sint Maarten',
        'SY': 'Syria',
        'SZ': 'Eswatini',
        'TC': 'Turks',
        'TD': 'Chad',
        'TF': 'Fr. S. Lands',
        'TG': 'Togo',
        'TH': 'Thailand',
        'TJ': 'Tajikistan',
        'TK': 'Tokelau',
        'TL': 'Timor-Leste',
        'TM': 'Turkmenistan',
        'TN': 'Tunisia',
        'TO': 'Tonga',
        'TR': 'Turkey',
        'TT': 'Trinidad',
        'TV': 'Tuvalu',
        'TW': 'Taiwan',
        'TZ': 'Tanzania',
        'UA': 'Ukraine',
        'UG': 'Uganda',
        'UM': 'U.S. Minor Outlying Islands',
        'US': 'United States',
        'UY': 'Uruguay',
        'UZ': 'Uzbekistan',
        'VA': 'Vatican City',
        'VC': 'St. Vincent',
        'VE': 'Venezuela',
        'VG': 'B. Virgin Is.',
        'VI': 'U.S. Virgin Is.',
        'VN': 'Vietnam',
        'VU': 'Vanuatu',
        'WF': 'Wallis',
        'WS': 'Samoa',
        'YE': 'Yemen',
        'YT': 'Mayotte',
        'ZA': 'South Africa',
        'ZM': 'Zambia',
        'ZW': 'Zimbabwe'
    }

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'MyApp/1.0'  # Example of a minimal User-Agent string
        }
        self.name = None
        self.api_key = None

    def load_api_key(self):
        try:
            with open('api_key.json', 'r') as f:
                api_keys = json.load(f)
                return api_keys.get(self.name)
        except Exception as e:
            print(f"Failed to load API key: {str(e)}")
            return False

    def send_request(self, endpoint, method='POST', params=None, data=None):
        try:
            url = self.base_url + endpoint

            if method == 'POST':
                response = requests.post(url, json=data, headers=self.headers, timeout=10)
            elif method == 'GET':
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
            else:
                return None

            if response.status_code == 200:
                return response.json()
            else:
                return None

        except requests.RequestException as e:
            print(f"Request exception occurred: {str(e)}")
            return None
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            return None


class IpApiCom(IPReputationClient):
    def __init__(self):
        base_url = "http://ip-api.com"
        super().__init__(base_url)
        self.batch_endpoint = "/batch"
        self.name = 'IpApiCom'

    def batch_get_ip_info(self, ips, fields=None, lang=None):
        try:
            endpoint = self.batch_endpoint

            # Constructing the JSON array for batch request
            requests_data = []
            for ip in ips:
                request_obj = {"query": ip}
                if fields:
                    request_obj["fields"] = fields
                if lang:
                    request_obj["lang"] = lang
                requests_data.append(request_obj)
            json_response = self.send_request(endpoint, method='POST', data=requests_data)
            # Sending POST request with JSON data
            return [{'IP': response['query'],
                     'Country': self.COUNTRY_CODES[response['countryCode']],
                     'Abuse': None,
                     'ISP': response['isp']} for response in json_response]

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            return None


class AbuseIPDB(IPReputationClient):
    def __init__(self):
        base_url = "https://api.abuseipdb.com/api/v2"
        super().__init__(base_url)
        self.name = "AbuseIPDB"
        self.check_endpoint = "/check"
        self.api_key = self.load_api_key()
        self.headers.update({'Key': self.api_key})

    def check_ip(self, ip, max_age_in_days=30):
        try:
            endpoint = self.check_endpoint
            querystring = {
                'ipAddress': ip,
                'maxAgeInDays': max_age_in_days
            }

            json_response = self.send_request(endpoint, method='GET', params=querystring)['data']
            return {'IP': json_response['ipAddress'],
                    'Country': self.COUNTRY_CODES[json_response['countryCode']],
                    'Abuse': json_response['abuseConfidenceScore'],
                    'ISP': json_response['isp']}

        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            return None

    def batch_get_ip_info(self, ips, max_age_in_days=30):
        results = []
        for ip in ips:
            result = self.check_ip(ip, max_age_in_days=max_age_in_days)
            if result:
                results.append(result)
        return results
