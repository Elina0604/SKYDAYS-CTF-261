
import { Routes } from '@angular/router';
import { HomePage } from './home-page/home-page';
import { SecretPage } from './secret-page/secret-page';

export const routes: Routes = [
    { path: '', component: HomePage },
    { path: 'hitcount', component: SecretPage }
];
