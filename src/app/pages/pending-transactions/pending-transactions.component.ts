import { Component, OnInit } from '@angular/core';
import { BlockchainService } from 'src/app/services/blockchain.service';
import { Router, ActivatedRoute } from '@angular/router';
@Component({
  selector: 'app-pending-transactions',
  templateUrl: './pending-transactions.component.html',
  styleUrls: ['./pending-transactions.component.scss']
})
export class PendingTransactionsComponent implements OnInit {
  public pendingTransactions = [];
  public miningInProgress = false;
  public justAddedTx = false;

  constructor(
    private blockChainService: BlockchainService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.pendingTransactions = blockChainService.getPendingTransactions();
  }

  ngOnInit() {
    if (this.route.snapshot.paramMap.get('addedTx')) {
      this.justAddedTx = true;

      setTimeout(() => {
        this.justAddedTx = false;
      }, 4000);
    }
  }

  minePendingTransactions() {
    this.miningInProgress = true;
    this.blockChainService.minePendingTransactions();
    this.miningInProgress = false;
    this.router.navigate(['/']);
  }
}
