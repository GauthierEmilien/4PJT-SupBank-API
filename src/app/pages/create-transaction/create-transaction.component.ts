import { Component, OnInit } from '@angular/core';
import {
  BlockchainService,
  IWalletKey
} from '../../services/blockchain.service';
import { Transaction } from '4pjt/blockchain';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-transaction',
  templateUrl: './create-transaction.component.html',
  styleUrls: ['./create-transaction.component.scss']
})
export class CreateTransactionComponent implements OnInit {
  public newTx = new Transaction();
  public ownWalletKey: IWalletKey;

  constructor(
    private blockChainService: BlockchainService,
    private router: Router
  ) {
    this.newTx = new Transaction();
    this.ownWalletKey = blockChainService.walletKeys[0];
  }

  ngOnInit() {
    this.newTx = new Transaction();
  }

  createTransaction() {
    const newTx = this.newTx;

    // Set the FROM address and sign the transaction
    newTx.fromAddress = this.ownWalletKey.publicKey;
    newTx.signTransaction(this.ownWalletKey.keyObj);

    try {
      this.blockChainService.addTransaction(this.newTx);
    } catch (e) {
      alert(e);
      return;
    }

    this.router.navigate(['/new/transaction/pending', { addedTx: true }]);
    this.newTx = new Transaction();
  }
}
