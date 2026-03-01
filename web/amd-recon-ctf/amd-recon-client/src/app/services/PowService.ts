import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class PowService {

  async solve(salt: string, answer: string): Promise<number> {
    let nonce = 0;
    
    while (true) {
      const data = salt + answer + nonce;
      const hash = await this.generateHash(data);

      if (hash.startsWith('0000') && '01234567'.includes(hash[4])) {
        return nonce;
      }

      nonce++;
      
      if (nonce % 20000 === 0) {
        await new Promise(resolve => setTimeout(resolve, 0));
      }
    }
  }

  private async generateHash(message: string): Promise<string> {
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    return Array.from(new Uint8Array(hashBuffer))
                .map(b => b.toString(16).padStart(2, '0'))
                .join('');
  }
}