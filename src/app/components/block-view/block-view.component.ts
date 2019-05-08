import { Component, OnInit, Input } from '@angular/core';
import { BlockchainService } from '../../services/blockchain.service';

@Component({
  selector: 'app-block-view',
  templateUrl: './block-view.component.html',
  styleUrls: ['./block-view.component.scss']
})
export class BlockViewComponent implements OnInit {
  @Input()
  public block;

  @Input()
  public selectedBlock;

  private blocksInChain;

  constructor(private blockChainService: BlockchainService) {
    this.blocksInChain = blockChainService.blockChainInstance.chain;
  }

  ngOnInit() {}

  blockHasTx() {
    return this.block.transactions.length > 0;
  }

  isSelectedBlock() {
    return this.block === this.selectedBlock;
  }

  getBlockNumber() {
    return this.blocksInChain.indexOf(this.block) + 1;
  }
}
