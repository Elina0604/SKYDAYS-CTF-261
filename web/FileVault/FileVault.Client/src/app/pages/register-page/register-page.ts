import { Component } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, ReactiveFormsModule, ValidationErrors, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { catchError, tap, throwError } from 'rxjs';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-register-page',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './register-page.html',
  styleUrl: './register-page.css',
})
export class RegisterPage {
  registerForm: FormGroup;

  constructor(private fb: FormBuilder, private authService: AuthService, private router: Router){
    this.registerForm = this.fb.group({
      userName: ['', [Validators.required, Validators.minLength(6), Validators.pattern('^[a-z0-9_]+$')]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required, , Validators.minLength(6)]],
    }, { 
      validators: this.passwordMatchValidator 
    });   
  }

  onSubmit(){
    if(this.registerForm.valid){
      this.authService.register({userName: this.registerForm.value.userName, password: this.registerForm.value.password})
        .pipe(
          tap(() => {
            this.router.navigate(['/login']);
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

  passwordMatchValidator(control: AbstractControl): ValidationErrors | null {
    const password = control.get('password');
    const confirmPassword = control.get('confirmPassword');

    if (password && confirmPassword && password.value !== confirmPassword.value) {
      confirmPassword.setErrors({ passwordMismatch: true });
      return { passwordMismatch: true };
    }
    return null;
  }
}
