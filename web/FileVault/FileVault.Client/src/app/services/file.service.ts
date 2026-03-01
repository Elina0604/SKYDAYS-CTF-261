import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { TokenService } from './token.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class FileService {
  apiUrl = `${environment.backendUrl}/api/file`

  constructor(private tokenService: TokenService, private http: HttpClient) {}

  getMyFileNames(): Observable<string[]> {
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.tokenService.getToken()}`);
    return this.http.get<string[]>(`${this.apiUrl}/GetMyFileNames`, { headers });
  }

  getMyUsedSpaceAsMB(): Observable<number> {
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.tokenService.getToken()}`);
    return this.http.get<number>(`${this.apiUrl}/GetMyUsedSpaceAsMB`, { headers });
  }

  download(fileName: string): Observable<{ blob: Blob; fileName: string }> {
    const headers = new HttpHeaders({ Authorization: `Bearer ${this.tokenService.getToken()}`});

    return this.http
      .get(`${this.apiUrl}/Download?fileName=${fileName}`, {headers, responseType: 'blob',observe: 'response'})
      .pipe(
        map(response => {
          return { blob: response.body as Blob, fileName };
        })
      );
  }

  uploadFile(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    const headers = new HttpHeaders({'Authorization': `Bearer ${this.tokenService.getToken()}`});
    return this.http.post<any>(`${this.apiUrl}/UploadFile`, formData, { headers });
  }

  delete(fileName: string): Observable<any> {
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.tokenService.getToken()}`);
    return this.http.delete<any>(`${this.apiUrl}/Delete?fileName=${fileName}`, { headers });
  }
}
