# 🚨 Security Policy

## 🔒 Reporting Security Vulnerabilities

We take the security of ConfluxAI seriously. If you discover a security vulnerability, please report it responsibly.

### 📧 How to Report

**Please DO NOT report security vulnerabilities through public GitHub issues.**

Instead, please send an email to: **security@confluxai.dev** with:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### ⏱️ Response Timeline

- **Initial Response**: Within 24 hours
- **Status Update**: Within 72 hours  
- **Resolution**: Within 30 days (depending on complexity)

### 🛡️ Security Measures

**Authentication & Authorization:**
- Session-based authentication
- Secure password hashing (bcrypt)
- Protected routes and API endpoints
- Input validation and sanitization

**Data Protection:**
- Environment variable protection
- Secure file upload handling
- XSS protection
- CSRF protection

**Infrastructure:**
- HTTPS enforcement
- Security headers
- Rate limiting
- Database connection security

### 🔄 Security Updates

Security updates are released as soon as possible after a vulnerability is confirmed and patched.

**Supported Versions:**

| Version | Supported |
|---------|-----------|
| 1.x.x   | ✅ |
| < 1.0   | ❌ |

### 🙏 Recognition

We acknowledge security researchers who help improve ConfluxAI's security:

- **Responsible Disclosure**: Credit in security advisories
- **Hall of Fame**: Recognition in our security page
- **Swag**: ConfluxAI merchandise for significant findings

### 📋 Security Checklist for Contributors

- [ ] No hardcoded secrets or API keys
- [ ] Input validation for all user inputs
- [ ] Proper error handling without information leakage
- [ ] Secure file upload handling
- [ ] Authentication checks for protected endpoints
- [ ] SQL injection prevention
- [ ] XSS protection in frontend code

Thank you for helping keep ConfluxAI secure! 🔒
