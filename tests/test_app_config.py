from config.app_config import APP_CONFIG

print("=" * 50)
print("Application Configuration Test")
print("=" * 50)

print(f"App Name      : {APP_CONFIG.APP_NAME}")
print(f"Version       : {APP_CONFIG.APP_VERSION}")
print(f"Author        : {APP_CONFIG.APP_AUTHOR}")
print(f"Currency      : {APP_CONFIG.DEFAULT_CURRENCY}")
print(f"Benchmark     : {APP_CONFIG.DEFAULT_BENCHMARK}")
print(f"Timezone      : {APP_CONFIG.TIMEZONE}")

print("\nSupported Assets:")

for asset in APP_CONFIG.SUPPORTED_ASSET_TYPES:
    print(f"  • {asset}")

print("\n✅ AppConfig loaded successfully.")