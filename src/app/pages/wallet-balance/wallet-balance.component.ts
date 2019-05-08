import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BlockchainService } from 'src/app/services/blockChain.service';

@Component({
  selector: 'app-wallet-balance',
  templateUrl: './wallet-balance.component.html',
  styleUrls: ['./wallet-balance.component.scss']
})
export class WalletBalanceComponent implements OnInit {
  public walletAddress = '';
  public balance = 0;
  public transactions = [];

  constructor(
    private route: ActivatedRoute,
    private blockChainService: BlockchainService
  ) {}

  ngOnInit() {
    this.route.params.subscribe(params => {
      // tslint:disable-next-line:no-string-literal
      this.walletAddress = params['address'];

      const blockChain = this.blockChainService.blockChainInstance;
      this.balance = blockChain.getBalanceOfAddress(this.walletAddress);
      this.transactions = blockChain.getAllTransactionsForWallet(
        this.walletAddress
      );
    });
  }
}
