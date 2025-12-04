import { Routes } from '@angular/router';
import { authGuard } from './guards/guard';

export const routes: Routes = [
  {
    path: 'products',
    loadComponent: () =>
      import('./pages/products/products.component').then(m => m.ProductsComponent),
    canActivate: [authGuard],
  },
  {
    path: 'login',
    loadComponent: () =>
      import('./pages/login/login.component').then(m => m.LoginComponent),
  },
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full',
  }
];
