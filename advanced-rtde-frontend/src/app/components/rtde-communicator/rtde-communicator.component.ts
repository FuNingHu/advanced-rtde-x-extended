import { TranslateService } from '@ngx-translate/core';
import { first } from 'rxjs/operators';
import { ChangeDetectionStrategy, ChangeDetectorRef, Component, inject, Input, OnChanges, OnInit, OnDestroy, SimpleChanges } from '@angular/core';
import { ApplicationPresenterAPI, ApplicationPresenter, RobotSettings } from '@universal-robots/contribution-api';
import { RtdeCommunicatorNode } from './rtde-communicator.node';
import { URCAP_ID, VENDOR_ID } from 'src/generated/contribution-constants';
import { BackendService } from './backend.service';
import { Subscription } from 'rxjs';
import { CdkDragDrop, moveItemInArray } from '@angular/cdk/drag-drop';

@Component({
    templateUrl: './rtde-communicator.component.html',
    styleUrls: ['./rtde-communicator.component.scss'],
    changeDetection: ChangeDetectionStrategy.Default,
    standalone: false,
})
export class RtdeCommunicatorComponent implements ApplicationPresenter, OnChanges, OnInit, OnDestroy {
    // applicationAPI is optional
    @Input() applicationAPI: ApplicationPresenterAPI;
    // robotSettings is optional
    @Input() robotSettings: RobotSettings;
    // applicationNode is required
    private _applicationNode: RtdeCommunicatorNode;
    private beService: BackendService = inject(BackendService);
    
    // Store data directly instead of using async pipe
    robotData: any = null;
    randomNumber: number | null = null;
    dataRate: number = 0;
    private messageCount: number = 0;
    private dataRateInterval?: ReturnType<typeof setInterval>;
    
    private dataSubscription?: Subscription;
    private randomNumberSubscription?: Subscription;

    private backendWebsocketUrl: string;
    private backendHttpUrl: string;

    protected outputs = ["DO 0", "DO 1", "DO 2", "DO 3", "DO 4", "DO 5", "DO 6", "DO 7"];
    protected output : string;

    dataCards = [
        { id: 'position', title: 'Position & Joints', type: 'position' },
        { id: 'io', title: 'I/O Signals', type: 'io' },
        { id: 'temperature', title: 'Temperature', type: 'temperature' },
        { id: 'others', title: 'Dynamics & Voltage', type: 'others' },
    ];

    constructor(
        protected readonly translateService: TranslateService,
        protected readonly cd: ChangeDetectorRef,
    ) {}

    // applicationNode is required
    get applicationNode(): RtdeCommunicatorNode {
        return this._applicationNode;
    }

    @Input()
    set applicationNode(value: RtdeCommunicatorNode) {
        this._applicationNode = value;
        this.cd.detectChanges();
    }

    // Getter for isMonitoring
    get isMonitoring(): boolean {
      return this.applicationNode.monitorState;
    }

    // Setter for isMonitoring
    set isMonitoring(value: boolean) {
      this.applicationNode.monitorState = value;
      this.saveNode();
    }

    ngOnInit(): void {
        // Subscribe to data stream
        this.dataSubscription = this.beService.data$.subscribe(data => {
            this.robotData = data;
            this.messageCount++;
            this.cd.detectChanges();
        });

        this.dataRateInterval = setInterval(() => {
            this.dataRate = this.messageCount;
            this.messageCount = 0;
            this.cd.detectChanges();
        }, 1000);

        // Subscribe to random number stream
        this.randomNumberSubscription = this.beService.randomNumber$.subscribe(num => {
            this.randomNumber = num;
            this.cd.detectChanges();
        });
    }

    ngOnDestroy(): void {
        if (this.dataSubscription) {
            this.dataSubscription.unsubscribe();
        }
        if (this.randomNumberSubscription) {
            this.randomNumberSubscription.unsubscribe();
        }
        if (this.dataRateInterval) {
            clearInterval(this.dataRateInterval);
        }
    }

    ngOnChanges(changes: SimpleChanges): void {
        // Initialize backend URLs when applicationAPI becomes available
        if (changes?.applicationAPI?.currentValue && changes.applicationAPI.firstChange) {
            this.backendWebsocketUrl = this.applicationAPI.getContainerContributionURL(VENDOR_ID, URCAP_ID, 'advanced-rtde-backend', 'websocket-api');
            this.backendHttpUrl = this.applicationAPI.getContainerContributionURL(VENDOR_ID, URCAP_ID, 'advanced-rtde-backend', 'rest-api');
            console.log('Backend URLs initialized:', {
                websocket: this.backendWebsocketUrl,
                http: this.backendHttpUrl
            });
        }

        if (changes?.robotSettings) {
            if (!changes?.robotSettings?.currentValue) {
                return;
            }

            if (changes?.robotSettings?.isFirstChange()) {
                if (changes?.robotSettings?.currentValue) {
                    this.translateService.use(changes?.robotSettings?.currentValue?.language);
                }
                this.translateService.setDefaultLang('en');
            }

            this.translateService
                .use(changes?.robotSettings?.currentValue?.language)
                .pipe(first())
                .subscribe(() => {
                    this.cd.detectChanges();
                });
        }

        if (changes?.applicationAPI && this.applicationAPI) {
            this.output = this.applicationNode.digitalOutput !== undefined
            ? this.outputs[this.applicationNode.digitalOutput] : "";
        }
    }

    startMonitoring(): void {
        console.log('Starting monitoring with URL:', this.backendWebsocketUrl);
        if (!this.backendWebsocketUrl) {
            console.error('Backend WebSocket URL is not initialized!');
            return;
        }
        this.isMonitoring = true;
        this.beService.connect(this.backendWebsocketUrl);
        this.cd.detectChanges();
    }

    stopMonitoring(): void {
        console.log('Stopping monitoring');
        this.isMonitoring = false;
        this.beService.disconnect();
        this.cd.detectChanges();
    }

    handleMonitoringToggle(): void {
        if (this.isMonitoring) {
            this.stopMonitoring();
        } else {
            this.startMonitoring();
        }
    }

    getRandomNumber(): void {
        this.beService.fetchRandomNumber(this.backendHttpUrl);
    }

    // call saveNode to save node parameters
    saveNode() {
        this.cd.detectChanges();
        this.applicationAPI.applicationNodeService.updateNode(this.applicationNode);
    }

    selectionChange($event){
        this.applicationNode.digitalOutput = this.outputs.indexOf($event);
        // Uncomment this to have the slider selection persist.
        // NOTE: Saving the application node will STOP any running programs.
        // this.saveNode();
        console.log(`Changed to DO${this.applicationNode.digitalOutput}`);
    }

    setDigitalOutput(value: number): void {
        if (this.applicationNode.digitalOutput !== undefined) {
            this.beService.setDigitalOutput(this.backendHttpUrl, this.applicationNode.digitalOutput, value);
        } else {
            console.error('Digital output is undefined.')
        }
      }

    // 拖拽处理
    drop(event: CdkDragDrop<string[]>) {
        moveItemInArray(this.dataCards, event.previousIndex, event.currentIndex);
    }

}
