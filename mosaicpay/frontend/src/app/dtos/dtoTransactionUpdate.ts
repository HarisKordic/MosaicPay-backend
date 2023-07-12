class dtoTransactionUpdate {
	type: string;
	amount: number;
	transaction_state: number;

	constructor() {
		this.type = "d";
		this.amount = 0;
		this.transaction_state = 0;
	}
}
