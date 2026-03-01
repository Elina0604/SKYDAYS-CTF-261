import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { TokenService } from '../../services/token.service';
import { NgOptimizedImage } from '@angular/common';

@Component({
  selector: 'app-navbar',
  imports: [RouterLink, NgOptimizedImage],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class Navbar {
  isLoggedIn: boolean = false;

  constructor(private router: Router, private tokenService: TokenService){
    this.tokenService.loggedIn$.subscribe((status: boolean) => {
      this.isLoggedIn = status;
    });
  }

  routeToMainPage(){
    this.router.navigate(['/']);
  }

  onLogout() {
    this.tokenService.clearToken();
    this.router.navigate(['/']);
  }
}
