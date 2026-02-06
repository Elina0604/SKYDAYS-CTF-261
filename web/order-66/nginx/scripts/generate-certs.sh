#!/bin/bash

# Script to generate self-signed SSL certificates for order66.skydays.ctf
# This creates certificates for local development with HTTPS support

CERT_DIR="$(dirname "$(dirname "$0")")/ssl"
DOMAIN="order66.skydays.ctf"
CERT_FILE="$CERT_DIR/cert.pem"
KEY_FILE="$CERT_DIR/key.pem"

echo "🔐 Generating self-signed SSL certificates for $DOMAIN..."

# Create SSL directory if it doesn't exist
mkdir -p "$CERT_DIR"

# Generate private key
echo "📋 Generating private key..."
openssl genrsa -out "$KEY_FILE" 2048

# Generate certificate signing request configuration
cat > /tmp/cert.conf <<EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = v3_req

[dn]
C=TR
ST=Istanbul
L=Istanbul
O=SKYDAYS CTF
OU=Order 66 Challenge
CN=$DOMAIN

[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = $DOMAIN
DNS.2 = *.skydays.ctf
DNS.3 = localhost
IP.1 = 127.0.0.1
EOF

# Generate self-signed certificate
echo "📜 Generating self-signed certificate..."
openssl req -new -x509 -key "$KEY_FILE" -out "$CERT_FILE" -days 365 \
    -config /tmp/cert.conf -extensions v3_req

# Set proper permissions
chmod 600 "$KEY_FILE"
chmod 644 "$CERT_FILE"

# Clean up
rm /tmp/cert.conf

echo "✅ SSL certificates generated successfully!"
echo "📁 Certificate: $CERT_FILE"
echo "🔑 Private key: $KEY_FILE"
echo ""
echo "🏠 To use these certificates locally, add this line to your /etc/hosts file:"
echo "127.0.0.1 order66.skydays.ctf"
echo ""
echo "⚠️  Note: You will see a security warning in your browser since this is a self-signed certificate."
echo "   This is normal for development. Click 'Advanced' and 'Proceed to order66.skydays.ctf'."
echo ""
echo "🚀 Your nginx server will now serve HTTPS traffic on https://order66.skydays.ctf/"