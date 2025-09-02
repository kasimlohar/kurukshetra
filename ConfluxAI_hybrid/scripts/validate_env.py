"""
Environment validation script for ConfluxAI
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def validate_environment():
    """Validate environment configuration"""
    logger.info("🔍 Validating ConfluxAI environment configuration...")
    
    # Load environment variables
    load_dotenv()
    
    # Required environment variables
    required_vars = {
        'DATABASE_URL': 'Database connection string',
        'HOST': 'Server host address',
        'PORT': 'Server port number',
        'UPLOAD_DIR': 'Upload directory path',
        'INDEX_DIR': 'Index directory path'
    }
    
    # Optional but recommended variables
    optional_vars = {
        'OPENAI_API_KEY': 'OpenAI API key for advanced AI features',
        'HUGGINGFACE_API_KEY': 'Hugging Face API key',
        'REDIS_URL': 'Redis connection for caching',
        'SECRET_KEY': 'Security key for sessions',
        'CORS_ORIGINS': 'Allowed CORS origins'
    }
    
    errors = []
    warnings = []
    
    print("\n" + "="*60)
    print("📋 REQUIRED CONFIGURATION")
    print("="*60)
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            # Hide sensitive information
            display_value = "***" if "key" in var.lower() or "password" in var.lower() or "url" in var.lower() else value
            print(f"✅ {var}: {display_value}")
            print(f"   📝 {description}")
        else:
            print(f"❌ {var}: NOT SET")
            print(f"   📝 {description}")
            errors.append(f"Missing required variable: {var}")
        print()
    
    print("="*60)
    print("🔧 OPTIONAL CONFIGURATION")
    print("="*60)
    
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value and value != f"your_{var.lower()}_here":
            display_value = "***" if "key" in var.lower() or "password" in var.lower() else value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"⚠️  {var}: NOT SET")
            warnings.append(f"Optional variable not set: {var}")
        print(f"   📝 {description}")
        print()
    
    # Check directories
    print("="*60)
    print("📂 DIRECTORY STRUCTURE")
    print("="*60)
    
    required_dirs = ['uploads', 'indexes', 'logs', 'temp']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/: EXISTS")
        else:
            print(f"❌ {dir_name}/: MISSING")
            try:
                os.makedirs(dir_name, exist_ok=True)
                print(f"   📁 Created {dir_name}/ directory")
            except Exception as e:
                errors.append(f"Failed to create directory {dir_name}: {e}")
    
    # Database URL validation
    print("\n" + "="*60)
    print("🗄️  DATABASE CONFIGURATION")
    print("="*60)
    
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        if "postgresql" in database_url:
            if "supabase" in database_url:
                print("✅ Database: PostgreSQL (Supabase)")
            else:
                print("✅ Database: PostgreSQL")
        elif "sqlite" in database_url:
            print("✅ Database: SQLite")
        else:
            print("⚠️  Database: Unknown type")
        
        # Check for asyncpg driver
        if "+asyncpg" in database_url:
            print("✅ Driver: AsyncPG (Async)")
        else:
            print("ℹ️  Driver: Standard (Sync)")
    else:
        errors.append("DATABASE_URL is required")
    
    # Summary
    print("\n" + "="*60)
    print("📊 VALIDATION SUMMARY")
    print("="*60)
    
    if errors:
        print("❌ VALIDATION FAILED")
        print(f"   {len(errors)} error(s) found:")
        for error in errors:
            print(f"   • {error}")
    else:
        print("✅ VALIDATION PASSED")
        print("   All required configuration is present")
    
    if warnings:
        print(f"\n⚠️  {len(warnings)} warning(s):")
        for warning in warnings:
            print(f"   • {warning}")
    
    print("\n" + "="*60)
    
    return len(errors) == 0

def main():
    """Main validation function"""
    success = validate_environment()
    
    if success:
        print("🎉 Environment validation completed successfully!")
        print("💡 You can now run: python setup_database.py")
        sys.exit(0)
    else:
        print("💥 Environment validation failed!")
        print("🔧 Please fix the errors above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
