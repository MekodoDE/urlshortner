import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api/api.service';

@Component({
  selector: 'app-redirect',
  templateUrl: './redirect.component.html',
  styleUrl: './redirect.component.scss'
})
export class RedirectComponent {
  response : any;
  
  constructor(private httpService: ApiService, private router: Router) { }

  ngOnInit() {
    this.httpService.getRedirect().subscribe(
      (response) => {
        this.response = response;
        if (this.response && this.response.redirect_url) {
          // Change the entire URL to the redirect_url
          window.location.href = this.response.redirect_url;
        } else {
          console.error('No redirect URL found in the response.');
        }
      },
      (error) => {
        console.log(error);
      }
    );
  }
}
