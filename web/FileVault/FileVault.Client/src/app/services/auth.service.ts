import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  apiUrl = `${environment.backendUrl}/api/auth`

  constructor(private http: HttpClient) {}

  login(loginRequest: LoginRequest): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/login`, loginRequest);
  }

  register(registerRequest: RegisterRequest): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/register`, registerRequest);
  }

  vipRegister(registerRequest: RegisterRequest): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/VIPRegister`, registerRequest);
  }
}
