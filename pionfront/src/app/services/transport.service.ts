import { EventEmitter, Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { User } from '../models/user';

@Injectable({
  providedIn: 'root'
})

export class TransportService {
  
  baseUrl = environment.baseUrl + "newpion/api/"

  public get accessToken(): string {
    return localStorage.getItem('accessToken');
  }

  public set accessToken(accessToken: string) {
    if (!accessToken)
      localStorage.removeItem('accessToken');
    else
      localStorage.setItem('accessToken', accessToken);
  }

  public get refreshToken(): string {
    return localStorage.getItem('refreshToken');
  }

  public set refreshToken(refreshToken: string) {
    if (!refreshToken)
      localStorage.removeItem('refreshToken');
    else
      localStorage.setItem('refreshToken', refreshToken);
  }

  public getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  constructor(private http: HttpClient, private router: Router) { }

  newUser: EventEmitter<boolean> = new EventEmitter()

  public user: User

  public sendToHeader(user) {
    this.newUser.emit(user);
  }

  public getToken(login: string, password: string): Promise<any> {
    //debugger;
    var formData: any = new FormData();
    formData.append("grant_type", "password");
    formData.append("username", login);
    formData.append("password", password);
    formData.append("client_id", "zHpEmzeZtngUwlu6v8sDhW8fuGdwi9sYLIem6NJ7");
    formData.append("client_secret", 'EEQxthdrmA1bUl4yWbbMgpgkyaVzec4aqBFUdF5k4toXlntqgenX7iRhP6ofICrx7HyS9NaWwtUfpmS9kViLiaoVAOLDS5PUdb8qCBD7BQ1DVf0gOmB65jfIUouceyiH');

    var result = this.http.post(this.baseUrl + "o/token/", formData, {
      headers: { 
        'Authorization': "Basic " + btoa("zHpEmzeZtngUwlu6v8sDhW8fuGdwi9sYLIem6NJ7:EEQxthdrmA1bUl4yWbbMgpgkyaVzec4aqBFUdF5k4toXlntqgenX7iRhP6ofICrx7HyS9NaWwtUfpmS9kViLiaoVAOLDS5PUdb8qCBD7BQ1DVf0gOmB65jfIUouceyiH") }
    });

    return new Promise<void>((resolve, reject) => 
      result.subscribe((responseData:any) => {
        this.accessToken = responseData.access_token;
        this.refreshToken = responseData.refresh_token;
        resolve();
      }, (error: HttpErrorResponse) => {
        reject(error);
      }));
  }

  private updateToken(): Promise<any> {
    if (!this.refreshToken) {
      this.router.navigate(['/auth/login']);
      return;
    }

    var formData: any = new FormData();
    formData.append("grant_type", "refresh_token");
    formData.append("refresh_token", this.refreshToken);
    formData.append("client_id", "zHpEmzeZtngUwlu6v8sDhW8fuGdwi9sYLIem6NJ7");
    formData.append("client_secret", "EEQxthdrmA1bUl4yWbbMgpgkyaVzec4aqBFUdF5k4toXlntqgenX7iRhP6ofICrx7HyS9NaWwtUfpmS9kViLiaoVAOLDS5PUdb8qCBD7BQ1DVf0gOmB65jfIUouceyiH");

    var result = this.http.post(this.baseUrl+"o/token/", formData);

    return new Promise((resolve, reject) =>
      result.subscribe((responseData:any) => {
        resolve(responseData);
      },
      (error: HttpErrorResponse) => {
        //debugger;
        this.accessToken = null;
        this.refreshToken = null;
      
        this.router.navigate(['/auth/login']);
        reject(error);
      }));
  }

  public post(type: string, request: any, anonymous: boolean = false):Promise<any> {
    if (!this.refreshToken && !anonymous) {
      //debugger;
      this.router.navigate(['/auth/login']);
      return;
    }

    // const csrftoken = this.getCookie('csrftoken');

    var result = this.http.post(this.baseUrl + type, request, {headers: {"Authorization": "Bearer " + this.accessToken}});

    return new Promise((resolve, reject) =>
      result.subscribe((responseData:any) => {
        resolve(responseData);
      },
      (error: HttpErrorResponse) => {
        //debugger;
        if (error.status == 401) {
          this.updateToken().then((data) => {
            this.accessToken = data.access_token;
            this.refreshToken = data.refresh_token;

            var secondaryResult = this.http.post(this.baseUrl+type, request, {headers: {"Authorization": "Bearer " + this.accessToken}});

            secondaryResult.subscribe((responseData:any) => {
              resolve(responseData);
            },
            (error: HttpErrorResponse) => {
              this.router.navigate(['/auth/login']);
              reject(error);
            });
          });
        }
        else {
          reject(error);
        }
      }));
  }

  public put(type: string, id: string, request: any):Promise<any> {
    if (!this.refreshToken) {
      //debugger;
      this.router.navigate(['/auth/login']);
      return;
    }

    // const csrftoken = this.getCookie('csrftoken');

    var result = this.http.put(this.baseUrl + type + id + "/", request, {headers: {"Authorization": "Bearer " + this.accessToken}});

    //debugger;
    
    return new Promise((resolve, reject) =>
          result.subscribe((responseData:any) => {
            resolve(responseData);
          },
          (error: HttpErrorResponse) => {
            //debugger;
            if (error.status == 401) {
              this.updateToken().then((data) => {
                this.accessToken = data.access_token;
                this.refreshToken = data.refresh_token;

                var secondaryResult = this.http.put(this.baseUrl+type + id + "/", request, {headers: {"Authorization": "Bearer " + this.accessToken}});

                secondaryResult.subscribe((responseData:any) => {
                  resolve(responseData);
                },
                (error: HttpErrorResponse) => {
                  this.router.navigate(['/auth/login']);
                  reject(error);
                });
              });
            }
            else {
              reject(error);
            }
          }));
  }

  public patch(type: string, id: string, request: any):Promise<any> {
    if (!this.refreshToken) {
      //debugger;
      this.router.navigate(['/auth/login']);
      return;
    }

    // const csrftoken = this.getCookie('csrftoken');

    var result = this.http.patch(this.baseUrl + type + id + "/", request, {headers: {"Authorization": "Bearer " + this.accessToken}});

    //debugger;
    
    return new Promise((resolve, reject) =>
          result.subscribe((responseData:any) => {
            resolve(responseData);
          },
          (error: HttpErrorResponse) => {
            //debugger;
            if (error.status == 401) {
              this.updateToken().then((data) => {
                this.accessToken = data.access_token;
                this.refreshToken = data.refresh_token;

                var secondaryResult = this.http.patch(this.baseUrl+type + id + "/", request, {headers: {"Authorization": "Bearer " + this.accessToken}});

                secondaryResult.subscribe((responseData:any) => {
                  resolve(responseData);
                },
                (error: HttpErrorResponse) => {
                  this.router.navigate(['/auth/login']);
                  reject(error);
                });
              });
            }
            else {
              reject(error);
            }
          }));
  }

  public get(type: string, anonymous: boolean = false):Promise<any> {
    if (!this.refreshToken && !anonymous) {
      //debugger;
      this.router.navigate(['/auth/login']);
      return;
    }

    var result = this.http.get(this.baseUrl+type, {headers: {"Authorization": "Bearer " + this.accessToken}});

    return new Promise((resolve, reject) =>
      result.subscribe((responseData:any) => {
        resolve(responseData);
      },
      (error: HttpErrorResponse) => {
        //debugger;
        if (error.status == 401) {
          this.updateToken().then((data) => {
            this.accessToken = data.access_token;
            this.refreshToken = data.refresh_token;

            var secondaryResult = this.http.get(this.baseUrl+type, {headers: {"Authorization": "Bearer " + this.accessToken}});

            secondaryResult.subscribe((responseData:any) => {
              resolve(responseData);
            },
            (error: HttpErrorResponse) => {
              this.router.navigate(['/auth/login']);
              reject(error);
            });
          });
        }
        else {
          reject(error);
        }
      }));
  }

  public getOld(type: string):Promise<any> {

    var result = this.http.get(type, {headers: {"Authorization": "Bearer " + this.accessToken}});

    return new Promise((resolve, reject) =>
          result.subscribe((responseData:any) => {
            resolve(responseData);
          },
          (error: HttpErrorResponse) => {
            //debugger;
            if (error.status == 401) {
              this.updateToken().then((data) => {
                this.accessToken = data.access_token;
                this.refreshToken = data.refresh_token;

                var secondaryResult = this.http.get(this.baseUrl+type, {headers: {"Authorization": "Bearer " + this.accessToken}});

                secondaryResult.subscribe((responseData:any) => {
                  resolve(responseData);
                },
                (error: HttpErrorResponse) => {
                  this.router.navigate(['/auth/login']);
                  reject(error);
                });
              });
            }
            else {
              reject(error);
            }
          }));
  }

  public getExact(type: string, index: string, anonymous: boolean = false):Promise<any> {
    if (!this.refreshToken && !anonymous) {
      this.router.navigate(['/auth/login']);
      return;
    }

    var result = this.http.get(this.baseUrl+type+'/' + index + '/', {headers: {"Authorization": "Bearer " + this.accessToken}});

    return new Promise((resolve, reject) =>
          result.subscribe((responseData:any) => {
            resolve(responseData);
          },
          (error: HttpErrorResponse) => {
            //debugger;
            if (error.status == 401) {
              this.updateToken().then((data) => {
                this.accessToken = data.access_token;
                this.refreshToken = data.refresh_token;

                var secondaryResult = this.http.get(this.baseUrl+type+'/' + index + '/', {headers: {"Authorization": "Bearer " + this.accessToken}});

                secondaryResult.subscribe((responseData:any) => {
                  resolve(responseData);
                },
                (error: HttpErrorResponse) => {
                  this.router.navigate(['/auth/login']);
                  reject(error);
                });
              });
            }
            else {
              reject(error);
            }
          }));
  }

  public delete(type: string, index: string):Promise<any> {
    if (!this.refreshToken) {
      this.router.navigate(['/auth/login']);
      return;
    }

    var result = this.http.delete(this.baseUrl+type+'/' + index + '/', {headers: {"Authorization": "Bearer " + this.accessToken}});

    return new Promise((resolve, reject) =>
          result.subscribe((responseData:any) => {
            resolve(responseData);
          },
          (error: HttpErrorResponse) => {
            //debugger;
            if (error.status == 401) {
              this.updateToken().then((data) => {
                this.accessToken = data.access_token;
                this.refreshToken = data.refresh_token;

                var secondaryResult = this.http.delete(this.baseUrl + type+'/' + index + '/', {headers: {"Authorization": "Bearer " + this.accessToken}});

                secondaryResult.subscribe((responseData:any) => {
                  resolve(responseData);
                },
                (error: HttpErrorResponse) => {
                  this.router.navigate(['/auth/login']);
                  reject(error);
                });
              });
            }
            else {
              reject(error);
            }
          }));
  }
}
