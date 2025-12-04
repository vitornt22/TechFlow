import { CanActivateFn, Router } from '@angular/router';
import { inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { PLATFORM_ID } from '@angular/core';

export const authGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const platformId = inject(PLATFORM_ID);

  // SSR check
  const isBrowser = isPlatformBrowser(platformId);

  // Se não estiver no navegador, bloqueia (SSR não tem token)
  if (!isBrowser) {
    return false;
  }

  const token = localStorage.getItem('access_token');

  if (token) {
    return true; // autorizado
  }

  // Se não tiver token → redireciona para o login
  router.navigate(['/login']);
  return false;
};
