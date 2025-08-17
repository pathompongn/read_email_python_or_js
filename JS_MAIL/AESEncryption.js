// import { jwtDecode } from "jwt-decode";
// import * as crypto from 'crypto-js';
const { jwtDecode } = require('jwt-decode');
const crypto = require('crypto-js');

class AESEncryption {

    static encrypt(value, token) {
        // Decode JWT token to extract userId
        let decoded = jwtDecode(token);
        let userId = decoded.sub;
        let keyValue = (userId ? userId : '').replace(/-/g, '');
        console.log("Encrypted Value: " + keyValue);
        // Ensure the key length is 16 bytes for AES
        let key = crypto.enc.Utf8.parse(keyValue);
        let ciphertext = crypto.AES.encrypt(value, key, { iv: key }).toString();
        return ciphertext;
    }
}

// Example usage
const token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJHYkczU05LRWc3VHBJUkc0SGFqY180LTY1YmxFVV9OcTYtYmJaNFY1c0ZZIn0.eyJleHAiOjE3MzQ3OTU1ODYsImlhdCI6MTczNDY4NzU4NiwianRpIjoiNDg3N2QyOWUtMmZjMi00NGQxLTk1ZTUtODdhNzY2NGIwMDY4IiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay11YXQudmF5dS1jbG91ZC5jb20vcmVhbG1zL25oc28tYXBwIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjMzNmU0YjE2LTkwZDAtNDJjMi04ZjhmLTgxYzYyNWZiZWI1MyIsInR5cCI6IkJlYXJlciIsImF6cCI6Im5oc28tYXBwLWNsaSIsInNlc3Npb25fc3RhdGUiOiJmZTJmYTMyNS01M2M4LTQxNzItYTA4Ni0yMTRhZWRmNzM4ZjkiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIi8qIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsImRlZmF1bHQtcm9sZXMtbmhzby1hcHAiLCJ1bWFfYXV0aG9yaXphdGlvbiIsIkxvYWR0ZXN0X-C4l-C4uOC4geC5gOC4guC4lV9FRElUT1IiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJzaWQiOiJmZTJmYTMyNS01M2M4LTQxNzItYTA4Ni0yMTRhZWRmNzM4ZjkiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJMb2FkdGVzdDEgdGVzdGVyIiwicHJlZmVycmVkX3VzZXJuYW1lIjoibG9hZHRlc3QwMSIsImdpdmVuX25hbWUiOiJMb2FkdGVzdDEiLCJmYW1pbHlfbmFtZSI6InRlc3RlciIsImVtYWlsIjoiYWxvbmdrb3JuLnllYW1yYXl1YisyQGtydW5ndGhhaS5jb20ifQ.Sjpp1v7B8F2RRkRUM8AI8CLBj6pcJ1-fiRgGj1q3qL5xPs6zf3LhsRxfceD9RG-mSnfsnzGuITdxTA86omTTPhRL64KFGazz3HUg8bi2AkoM1H5vi68WDMcYb5TU7P-yjX-Ug52OrGXSwnKlEhukhHKeGafblBzTW0caiPF0YxbB5NaZl_H-tjYZIswSusr4kXf_9SJBb4Ujht06rRSXALN6Su3aesckNZQz5Q_x4afdHdSzGhsSM0KGhuGu7V-WJ-8AFR-yILKo58fFTU4YCdrXu0NLDixzDUILwXPeysuwtijriEjgjUvC0s8pHzvhTl4obY7aI0cQml0dchkg";
const value = "2220";
const encryptedValue = AESEncryption.encrypt(value, token);
console.log("Encrypted Value: " + encryptedValue);
