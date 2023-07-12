class dtoAccountTransaction {
	accountName: string;
	transactionAmount: string;
	transactionType: string;
	transactionState: string;
	accountId: string;
	transactionId: string;
	documentUrl?: string;
	documentType?: string;

	constructor() {
		this.accountName = "";
		this.transactionAmount = "";
		this.transactionType = "";
		this.transactionState = "";
		this.transactionId = "";
		this.accountId = "";
		this.documentUrl = "";
		this.documentType = "";
	}
}
