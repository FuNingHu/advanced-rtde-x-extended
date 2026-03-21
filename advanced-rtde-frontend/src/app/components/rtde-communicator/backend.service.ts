import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BackendService {
  private socket: WebSocket | null = null;
  private dataSubject: BehaviorSubject<any> = new BehaviorSubject(null);
  private randomNumberSubject: BehaviorSubject<number | null> = new BehaviorSubject<number | null>(null);
  
  public readonly data$: Observable<any> = this.dataSubject.asObservable();
  public readonly randomNumber$: Observable<number | null> = this.randomNumberSubject.asObservable();
  
  private protocol: string = 'ws://';
  private isConnecting: boolean = false;

  constructor(private http: HttpClient) {}

  connect(url: string): void {
    if (this.isConnecting) {
      console.log('Already connecting...');
      return;
    }

    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected');
      return;
    }

    this.isConnecting = true;
    const wsUrl = this.protocol + url + '/ws';
    console.log('Connecting to WebSocket:', wsUrl);

    this.socket = new WebSocket(wsUrl);
    
    this.socket.onopen = () => {
      console.log('WebSocket connection opened successfully');
      this.isConnecting = false;
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        // console.log('Received data from WebSocket:', data); // 注释掉频繁输出
        this.dataSubject.next(data);
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
      this.isConnecting = false;
    };

    this.socket.onclose = (event) => {
      console.log('WebSocket connection closed:', event.code, event.reason);
      this.isConnecting = false;
      this.socket = null;
    };
  }

  disconnect(): void {
    if (this.socket) {
      console.log('Disconnecting WebSocket');
      this.socket.close();
      this.socket = null;
      this.dataSubject.next(null);
    }
  }

  fetchRandomNumber(url: string): void {
    const fullUrl = 'http://' + url + '/random-number';
    this.http.get<{ random_number: number }>(fullUrl).subscribe(response => {
      this.randomNumberSubject.next(response.random_number);
    });
  }

  setDigitalOutput(url: string, digitalOutput: number, value: number, offset: number = 0): void {
    const fullUrl = 'http://' + url + '/set-digital-output';
    this.http.post(fullUrl, { digital_output: digitalOutput, value: value, offset: offset }).subscribe();
  }

}