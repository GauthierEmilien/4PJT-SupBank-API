import { Component, OnInit } from '@angular/core';
import { BlockchainService } from '../..//services/blockchain.service';

@Component({
  selector: 'app-blockchain-viewer',
  templateUrl: './blockchain-viewer.component.html',
  styleUrls: ['./blockchain-viewer.component.scss']
})
export class BlockchainViewerComponent implements OnInit {
  public blocks = [];
  public selectedBlock = null;

  constructor(private blockChainService: BlockchainService) {
    this.blocks = blockChainService.blockChainInstance.chain;
    this.selectedBlock = this.blocks[0];
    console.log(this.blocks);
  }

  ngOnInit() {}

  showTransactions(block) {
    console.log(block);
    this.selectedBlock = block;
    return false;
  }

  blockHasTx(block) {
    return block.transactions.length > 0;
  }

  selectedBlockHasTx() {
    return this.blockHasTx(this.selectedBlock);
  }

  isSelectedBlock(block) {
    return this.selectedBlock === block;
  }

  getBlockNumber(block) {
    return this.blocks.indexOf(block) + 1;
  }
}
