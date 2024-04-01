import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../../../services/api/api.service';

@Component({
  selector: 'app-url-edit',
  templateUrl: './url-edit.component.html',
  styleUrl: './url-edit.component.scss'
})
export class UrlEditComponent {
  currentUrlKey: string = '';
  urlKey: string = '';
  redirectUrl: string = '';

  constructor(private route: ActivatedRoute, private apiService: ApiService, private router: Router) { }

  ngOnInit() {
    // Get URL key from route parameters
    this.route.params.subscribe(params => {
      const urlKey = params['urlKey'];
      if (urlKey) {
        // Fetch URL details from API based on URL key
        this.currentUrlKey = urlKey;
        this.apiService.getUrl(urlKey).subscribe(
          (url: any) => {
            this.urlKey = url.url_key;
            this.redirectUrl = url.redirect_url;
          },
          error => {
            console.error('Error fetching URL:', error);
          }
        );
      }
    });
  }

  onSubmit() {
    const updatedUrl = {
      url_key: this.urlKey,
      redirect_url: this.redirectUrl
    };

    this.apiService.updateUrl(this.currentUrlKey, updatedUrl).subscribe(
      () => {
        // Redirect to the URLs list after successful update
        this.router.navigate(['/urls']);
      },
      (error) => {
        console.error('Error updating URL:', error);
      }
    );
  }
}
