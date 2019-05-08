import { Component, OnInit } from '@angular/core';
import { BlockchainService } from 'src/app/services/blockchain.service';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent implements OnInit {
  public blockChain;

  constructor(private blockChainService: BlockchainService) {
    this.blockChain = blockChainService.blockChainInstance;
  }

  ngOnInit() {}
}
