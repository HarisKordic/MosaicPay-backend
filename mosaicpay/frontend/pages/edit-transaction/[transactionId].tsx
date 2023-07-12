import React, { useState } from "react";
import {
	Alert,
	Box,
	Button,
	Container,
	FormControlLabel,
	Grid,
	InputLabel,
	MenuItem,
	Radio,
	RadioGroup,
	Select,
	Slider,
	Typography,
} from "@mui/material";
import { useRouter } from "next/router";
import { useEffect } from "react";
import {
	deleteTransaction,
	getTransaction,
	getUserAccounts,
	postNewTransaction,
	putTransaction,
} from "../../src/app/api";
import { Cancel, Delete, Save } from "@mui/icons-material";
import AccountMenu from "@/app/components/AccountMenu";

export default function EditTransaction() {
	const [showAlert, setShowAlert] = useState(false);
	const [transactionState, setTransactionState] = useState(1);
	const [accountState, setAccountState] = useState([]);
	const [selectedAccount, setSelectedAccount] = useState("");
	const [amountState, setAmountState] = useState(1000);
	const [alertMessage, setAlertMessage] = useState("");
	const [transactionType, setTransactionType] = useState("");
	const router = useRouter();
	const { transactionId } = router.query;

	const getTransactionData = async () => {
		const data = await getTransaction(transactionId);
		return data;
	};
	let data: dtoTransaction;
	const setStates = async () => {
		try {
			if (transactionId) {
				data = await getTransactionData();
				setTransactionType(data.type);
				setAmountState(data.amount);
				setTransactionState(data.transaction_state);
			}
		} catch (error) {
			router.push("/404");
		}
	};

	useEffect(() => {
		setStates();
	}, [transactionId]);
	useEffect(() => {
		const getData = async () => {
			const data = await getUserAccounts();
			const accounts = data.map((item: any) => ({
				value: item.account_id,
				name: item.name,
			}));
			setAccountState(accounts);
			if (accounts.length > 0) {
				setSelectedAccount(accounts[0].value);
			}
		};

		getData();
	}, []);

	const handleSubmit = async () => {
		try {
			const transaction: dtoTransactionUpdate = {
				type: transactionType,
				amount: amountState,
				transaction_state: transactionState,
			};
			await putTransaction(transactionId, transaction);
			setShowAlert(true);
			setAlertMessage("Transaction successfuly updated!");
			setStates();
			return;
		} catch (error) {}
	};

	const handleAccountChange = (event: any) => {
		setSelectedAccount(event.target.value);
	};

	const handleDelete = async () => {
		try {
			await deleteTransaction(transactionId);
			setShowAlert(true);
			setAlertMessage("Transaction is successfuly deleted!");
		} catch (error) {}
	};
	return (
		<Container disableGutters>
			<Box display={"flex"} justifyContent={"center"}>
				<AccountMenu></AccountMenu>
			</Box>
			<Grid
				display="flex"
				flexDirection="column"
				width="100%"
				height="100%"
				justifyContent="center"
				padding={2}
				mt={2}
			>
				<Box>
					<Typography variant="h4" component="h4" sx={{ textAlign: "center" }}>
						Edit transaction
					</Typography>
				</Box>
				<Box width="100%" padding={2}>
					<Box mt={3}>
						<InputLabel id="transaction-state-simple-select-label">
							Transaction type
						</InputLabel>
						<RadioGroup
							aria-labelledby="transaction-type-radio-buttons-group-label"
							value={transactionType}
							name="transaction-type-radio-buttons-group"
							onChange={(event) => setTransactionType(event.target.value)}
						>
							<FormControlLabel
								value="D"
								control={<Radio color="secondary" />}
								label="Debit"
							/>
							<FormControlLabel
								value="C"
								control={<Radio color="secondary" />}
								label="Credit"
								color="secondary"
							/>
						</RadioGroup>
					</Box>
					<Box mt={3}>
						<InputLabel>Amount</InputLabel>
						<Slider
							max={10000}
							size="medium"
							defaultValue={1000}
							aria-label="Medium"
							valueLabelDisplay="auto"
							color="secondary"
							onChange={(e: any) => setAmountState(e.target.value)}
						/>
					</Box>
					<Box mt={3}>
						<InputLabel id="account-state-simple-select-label">
							Account
						</InputLabel>
						<Select
							fullWidth
							labelId="account-state-select-label"
							id="account-state-select"
							name="account-state"
							value={selectedAccount}
							label="Account state"
							onChange={handleAccountChange}
							color="secondary"
						>
							{accountState.map((account: any) => (
								<MenuItem value={account.value} key={account.value}>
									{account.name}
								</MenuItem>
							))}
						</Select>
					</Box>
					<Box mt={3}>
						<InputLabel id="transaction-state-simple-select-label">
							Transaction state
						</InputLabel>
						<Select
							fullWidth
							labelId="transaction-state-select-label"
							id="transaction-state-select"
							name="transaction-state"
							value={transactionState}
							label="Transaction state"
							onChange={(e: any) => setTransactionState(e.target.value)}
							color="secondary"
						>
							<MenuItem value={1}>Draft</MenuItem>
							<MenuItem value={2}>Pending</MenuItem>
							<MenuItem value={3}>Processed</MenuItem>
							<MenuItem value={4}>Failed</MenuItem>
						</Select>
					</Box>
					<Alert
						sx={{ mt: 5, display: showAlert ? "flex" : "none" }}
						action={
							<Button
								color="success"
								size="small"
								onClick={() => setShowAlert(false)}
							>
								X
							</Button>
						}
						onClose={() => setShowAlert(false)}
						severity="success"
					>
						{alertMessage}
					</Alert>
					<Box
						display={"flex"}
						justifyContent={"space-between"}
						sx={{ mt: 10 }}
					>
						<Button
							startIcon={<Save></Save>}
							color="secondary"
							variant="outlined"
							onClick={handleSubmit}
						>
							Save
						</Button>
						<Button
							startIcon={<Delete></Delete>}
							color="secondary"
							variant="outlined"
							onClick={() => handleDelete()}
						>
							Delete
						</Button>
					</Box>
				</Box>
			</Grid>
		</Container>
	);
}
