#!/usr/bin/env python3
"""
API Consumer - Fetch and process data from various APIs
Supports: REST APIs, JSON/XML responses, authentication, rate limiting, data export
"""

import requests
import json
import csv
import time
from pathlib import Path
from datetime import datetime
import argparse
from typing import Dict, List, Optional


class APIConsumer:
    """Generic API consumer with common functionality"""
    
    def __init__(self, base_url: str, headers: Optional[Dict] = None):
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make GET request to API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            return {}
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make POST request to API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.post(url, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ API Error: {e}")
            return {}


def fetch_github_repos(username: str, max_repos: int = 10):
    """Fetch public repositories from GitHub"""
    print(f"\n🔍 Fetching GitHub repositories for user: {username}")
    
    api = APIConsumer("https://api.github.com")
    repos = api.get(f"users/{username}/repos", params={
        'sort': 'updated',
        'per_page': max_repos
    })
    
    if not repos:
        print("❌ No repositories found or API error")
        return []
    
    print(f"✅ Found {len(repos)} repositories\n")
    
    repo_data = []
    for repo in repos:
        repo_info = {
            'name': repo.get('name'),
            'description': repo.get('description', 'No description'),
            'language': repo.get('language', 'Unknown'),
            'stars': repo.get('stargazers_count', 0),
            'forks': repo.get('forks_count', 0),
            'url': repo.get('html_url'),
            'updated': repo.get('updated_at', '')
        }
        repo_data.append(repo_info)
        
        print(f"📦 {repo_info['name']}")
        print(f"   ⭐ {repo_info['stars']} stars | 🍴 {repo_info['forks']} forks | 💻 {repo_info['language']}")
        print(f"   {repo_info['description'][:80]}...")
        print(f"   🔗 {repo_info['url']}\n")
    
    return repo_data


def fetch_weather(city: str, api_key: Optional[str] = None):
    """Fetch weather data from OpenWeatherMap API"""
    print(f"\n🌤️  Fetching weather for: {city}")
    
    if not api_key:
        print("⚠️  No API key provided. Using demo mode with mock data.")
        print("💡 Get a free API key at: https://openweathermap.org/api\n")
        
        # Mock data for demonstration
        return {
            'city': city,
            'temperature': 22.5,
            'feels_like': 21.8,
            'description': 'Partly cloudy',
            'humidity': 65,
            'wind_speed': 3.5,
            'timestamp': datetime.now().isoformat()
        }
    
    api = APIConsumer("https://api.openweathermap.org/data/2.5")
    data = api.get("weather", params={
        'q': city,
        'appid': api_key,
        'units': 'metric'
    })
    
    if not data:
        return {}
    
    weather_info = {
        'city': data.get('name'),
        'temperature': data['main'].get('temp'),
        'feels_like': data['main'].get('feels_like'),
        'description': data['weather'][0].get('description'),
        'humidity': data['main'].get('humidity'),
        'wind_speed': data['wind'].get('speed'),
        'timestamp': datetime.now().isoformat()
    }
    
    print(f"🌡️  Temperature: {weather_info['temperature']}°C (feels like {weather_info['feels_like']}°C)")
    print(f"☁️  Conditions: {weather_info['description']}")
    print(f"💧 Humidity: {weather_info['humidity']}%")
    print(f"💨 Wind Speed: {weather_info['wind_speed']} m/s\n")
    
    return weather_info


def fetch_crypto_prices(symbols: List[str] = ['bitcoin', 'ethereum', 'cardano']):
    """Fetch cryptocurrency prices from CoinGecko API"""
    print(f"\n💰 Fetching cryptocurrency prices...")
    
    api = APIConsumer("https://api.coingecko.com/api/v3")
    
    crypto_data = []
    
    for symbol in symbols:
        print(f"   Fetching {symbol}...")
        data = api.get(f"coins/{symbol}")
        
        if data:
            crypto_info = {
                'name': data.get('name'),
                'symbol': data.get('symbol', '').upper(),
                'current_price': data['market_data']['current_price'].get('usd'),
                'market_cap': data['market_data'].get('market_cap', {}).get('usd'),
                'price_change_24h': data['market_data'].get('price_change_percentage_24h'),
                'high_24h': data['market_data']['high_24h'].get('usd'),
                'low_24h': data['market_data']['low_24h'].get('usd'),
                'timestamp': datetime.now().isoformat()
            }
            crypto_data.append(crypto_info)
            
            change_emoji = "📈" if crypto_info['price_change_24h'] > 0 else "📉"
            print(f"\n   {crypto_info['name']} ({crypto_info['symbol']})")
            print(f"   💵 Price: ${crypto_info['current_price']:,.2f}")
            print(f"   {change_emoji} 24h Change: {crypto_info['price_change_24h']:.2f}%")
            print(f"   📊 24h Range: ${crypto_info['low_24h']:,.2f} - ${crypto_info['high_24h']:,.2f}")
        
        # Rate limiting - be nice to the API
        time.sleep(1)
    
    return crypto_data


def export_to_json(data: List[Dict], filename: str):
    """Export data to JSON file"""
    filepath = Path(filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Data exported to: {filepath.absolute()}")


def export_to_csv(data: List[Dict], filename: str):
    """Export data to CSV file"""
    if not data:
        print("⚠️  No data to export")
        return
    
    filepath = Path(filename)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    print(f"💾 Data exported to: {filepath.absolute()}")


def main():
    parser = argparse.ArgumentParser(
        description='Consume various APIs and export data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch GitHub repositories
  python api_consumer.py github --username torvalds
  
  # Fetch weather (demo mode)
  python api_consumer.py weather --city "London"
  
  # Fetch cryptocurrency prices
  python api_consumer.py crypto --symbols bitcoin ethereum solana
  
  # Export to JSON
  python api_consumer.py github --username octocat --export json --output repos.json
  
  # Export to CSV
  python api_consumer.py crypto --export csv --output crypto_prices.csv
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='API to consume')
    
    # GitHub command
    github_parser = subparsers.add_parser('github', help='Fetch GitHub repositories')
    github_parser.add_argument('--username', required=True, help='GitHub username')
    github_parser.add_argument('--max-repos', type=int, default=10, help='Maximum repositories to fetch')
    
    # Weather command
    weather_parser = subparsers.add_parser('weather', help='Fetch weather data')
    weather_parser.add_argument('--city', required=True, help='City name')
    weather_parser.add_argument('--api-key', help='OpenWeatherMap API key (optional)')
    
    # Crypto command
    crypto_parser = subparsers.add_parser('crypto', help='Fetch cryptocurrency prices')
    crypto_parser.add_argument('--symbols', nargs='+', default=['bitcoin', 'ethereum', 'cardano'],
                              help='Cryptocurrency symbols')
    
    # Export options (common to all commands)
    for subparser in [github_parser, weather_parser, crypto_parser]:
        subparser.add_argument('--export', choices=['json', 'csv'], help='Export format')
        subparser.add_argument('--output', help='Output filename')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    data = []
    
    if args.command == 'github':
        data = fetch_github_repos(args.username, args.max_repos)
    
    elif args.command == 'weather':
        weather_data = fetch_weather(args.city, args.api_key)
        if weather_data:
            data = [weather_data]
    
    elif args.command == 'crypto':
        data = fetch_crypto_prices(args.symbols)
    
    # Export if requested
    if args.export and data:
        if not args.output:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            args.output = f"{args.command}_data_{timestamp}.{args.export}"
        
        if args.export == 'json':
            export_to_json(data, args.output)
        elif args.export == 'csv':
            export_to_csv(data, args.output)


if __name__ == '__main__':
    main()
