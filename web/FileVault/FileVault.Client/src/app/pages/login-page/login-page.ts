import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { catchError, tap, throwError } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';
import { TokenService } from '../../services/token.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login-page',
  imports: [ReactiveFormsModule],
  templateUrl: './login-page.html',
  styleUrl: './login-page.css',
})
export class LoginPage {
  loginForm: FormGroup;

  constructor(private fb: FormBuilder, private authService: AuthService, private tokenService: TokenService, private router: Router){
    this.loginForm = this.fb.group({
      userName: ['', [Validators.required, Validators.minLength(6), Validators.pattern('^[a-z0-9_]+$')]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });   
  }

  onSubmit(){
    if(this.loginForm.valid){
      this.authService.login({userName: this.loginForm.value.userName, password: this.loginForm.value.password})
        .pipe(
          tap((response) => {
            this.tokenService.setToken(response.token);
            this.router.navigate(['/my-vault']);
          }),
          catchError((err: HttpErrorResponse) => {
            const message = err.error?.error?.message ?? 'Beklenmeyen bir hata oluştu';
            window.alert(message);
            return throwError(() => err);
          })
        )
        .subscribe();
    }
  }
}
