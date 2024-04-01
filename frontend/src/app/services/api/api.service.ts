import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  urlKey = '';

  constructor(private http: HttpClient, private router: Router) {
    const urlParts = this.router.url.split('/');
    // Remove the first element which is an empty string
    urlParts.shift();
    // Return the first segment of the URL (excluding the domain and protocol)
    this.urlKey = urlParts[0];
  }

  getRedirect() {
    const url = `${environment.apiUrl}${this.urlKey}`;
    return this.http.get(url);
  }

  getUrls() {
    const url = `${environment.apiUrl}`;
    return this.http.get(url);
  }

  getUrl(urlKey: string) {
    const url = `${environment.apiUrl}${urlKey}`;
    return this.http.get(url);
  }

  createUrl(newUrl: any) {
    const url = `${environment.apiUrl}`;
    return this.http.post(url, newUrl);
  }

  updateUrl(urlKey: string, newUrl: any) {
    const url = `${environment.apiUrl}${urlKey}`;
    return this.http.put(url, newUrl);
  }

  deleteUrl(urlKey: string) {
    const url = `${environment.apiUrl}${urlKey}`;
    return this.http.delete(url);
  }
}
