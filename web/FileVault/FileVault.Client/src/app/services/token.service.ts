import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class TokenService {
  private readonly TOKEN_KEY = 'token';
  private readonly ROLE_KEY = 'role';
  private readonly USER_NAME_KEY = 'user_name';
  private readonly ID_KEY = 'id';
  private readonly TOKEN_EXP_KEY = 'token_exp';
  private loggedInSubject = new BehaviorSubject<boolean>(this.isLoggedIn());
  loggedIn$ = this.loggedInSubject.asObservable();

  setToken(token: string) {
    const payload = JSON.parse(atob(token.split('.')[1]));

    const expDate = new Date(payload.exp * 1000);
    const hours = expDate.getHours().toString().padStart(2, '0');
    const minutes = expDate.getMinutes().toString().padStart(2, '0');

    sessionStorage.setItem(this.TOKEN_KEY, token);
    sessionStorage.setItem(this.TOKEN_EXP_KEY, `${hours}:${minutes}`);
    sessionStorage.setItem(this.ROLE_KEY, payload.role);
    sessionStorage.setItem(this.USER_NAME_KEY, payload.user_name);
    sessionStorage.setItem(this.ID_KEY, payload.sub);
    this.loggedInSubject.next(true);
  }

  getToken(): string | null {
    return sessionStorage.getItem(this.TOKEN_KEY);
  }

  getTokenExpTime(){
    return sessionStorage.getItem(this.TOKEN_EXP_KEY);
  }

  clearToken() {
    sessionStorage.removeItem(this.TOKEN_KEY);
    sessionStorage.removeItem(this.ROLE_KEY);
    sessionStorage.removeItem(this.USER_NAME_KEY);
    sessionStorage.removeItem(this.ID_KEY);
    sessionStorage.removeItem(this.TOKEN_EXP_KEY);
    this.loggedInSubject.next(false);
  }

  isLoggedIn(): boolean {
    return this.getToken() !== null;
  }

  getRole(): string | null {
    return sessionStorage.getItem(this.ROLE_KEY);
  }

  getUserName(): string | null {
    return sessionStorage.getItem(this.USER_NAME_KEY);
  }

  getId(): string | null {
    return sessionStorage.getItem(this.ID_KEY);
  }
}
