import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../../services/api/api.service';

@Component({
  selector: 'app-url-create',
  templateUrl: './url-create.component.html',
  styleUrl: './url-create.component.scss'
})
export class UrlCreateComponent {
  urlKey: string = '';
  redirectUrl: string = '';

  constructor(private apiService: ApiService, private router: Router) { }

  onSubmit() {
    const newUrl = {
      owner_id: 1,
      url_key: this.urlKey,
      redirect_url: this.redirectUrl
    };

    this.apiService.createUrl(newUrl).subscribe(
      () => {
        // Redirect to the URLs list after successful creation
        this.router.navigate(['/urls']);
      },
      (error) => {
        console.error('Error creating URL:', error);
      }
    );
  }
}
