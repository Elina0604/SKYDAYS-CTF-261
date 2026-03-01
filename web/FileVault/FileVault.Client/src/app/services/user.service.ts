import { Injectable } from '@angular/core';
import { TokenService } from './token.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map, Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  apiUrl = `${environment.backendUrl}/api/user`

  constructor(private tokenService: TokenService, private http: HttpClient) {}

  goVIP(): Observable<any> {
    const headers = new HttpHeaders({ Authorization: `Bearer ${this.tokenService.getToken()}`});
    return this.http.post<any>(`${this.apiUrl}/login`, {}, {headers});
  }
}
