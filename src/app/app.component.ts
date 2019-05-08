import { Component, OnInit } from '@angular/core';
import { BlockchainService } from './services/blockchain.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'MaxoteCoin';
  public blockChain;
  public showInfoMessage = true;

  constructor(private blockChainService: BlockchainService) {
    this.blockChain = blockChainService.blockChainInstance;
  }

  ngOnInit(): void {}

  thereArePendingTransactions() {
    return this.blockChain.pendingTransactions.length > 0;
  }

  dismissInfoMessage() {
    this.showInfoMessage = false;
  }
}
