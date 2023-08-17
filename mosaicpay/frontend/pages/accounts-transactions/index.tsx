import { Box, Container, Grid, IconButton, Typography } from "@mui/material";
import AccountMenu from "../../src/app/components/AccountMenu";
import { Add } from "@mui/icons-material";
import MainCard from "@/app/components/MainCard";
import { useRouter } from "next/router";
import { getAccountsTransactions } from "@/app/api";
import { useEffect, useState } from "react";
import { stat } from "fs";

export default function AccountsTransactions() {
	const router = useRouter();
	const [accountsTransactions, setAccountsTransactions] = useState<
		dtoAccountTransaction[]
	>([]);

	const convertTransactionState = (state: number): string => {
		switch (state) {
			case 1:
				return "Draft";
			case 2:
				return "Pending";
			case 3:
				return "Processed";
			case 4:
				return "Failed";
		}
		return "";
	};
	const fetchData = async () => {
		try {
			const data = await getAccountsTransactions();

			const updatedTransactions = data.map((item: any) => ({
				accountName: item.account.name,
				transactionAmount: item.amount,
				transactionState: convertTransactionState(item.transaction_state),
				transactionType: item.type,
				transactionId: item.transaction_id,
				accountId: item.account.account_id,
				documentUrl: item?.document.url,
				documentType: item?.document.type,
			}));
			setAccountsTransactions(updatedTransactions);
		} catch (error) {}
	};

	useEffect(() => {
		fetchData();
	}, []);

	return (
		<Container disableGutters>
			<Box display={"flex"} justifyContent={"center"}>
				<AccountMenu></AccountMenu>
			</Box>
			<Grid
				display={"flex"}
				flexDirection={"column"}
				sx={{ width: "100%" }}
				justifyContent={"center"}
				padding={5}
			>
				<Box>
					<Typography
						variant="h6"
						component={"h6"}
						sx={{ textAlign: "center" }}
						fontWeight={"bold"}
					>
						Accounts & Transactions
					</Typography>
				</Box>
				<Box
					width={"100%"}
					padding={0}
					mt={5}
					sx={{
						maxHeight: "600px",
						overflowY: "auto",
					}}
				>
					{accountsTransactions.length > 0 ? (
						accountsTransactions.map((item: dtoAccountTransaction) => (
							<MainCard
								key={item.accountId}
								accountName={item.accountName}
								transactionAmount={item.transactionAmount}
								transactionType={item.transactionType}
								transactionState={item.transactionState}
								transactionId={item.transactionId}
								accountId={item.accountId}
								documentUrl={item?.documentUrl}
								documentType={item?.documentType}
							></MainCard>
						))
					) : (
						<Typography>
							Oops... It seems you don't have any transactions yet. Make your
							first one by clicking on the button "Add transaction"
						</Typography>
					)}
				</Box>

				<Box
					display={"flex"}
					flexDirection={"row"}
					width={"100%"}
					justifyContent={"space-between"}
					mt={3}
					mb={3}
				>
					<IconButton
						aria-label="add-account"
						size="large"
						color="secondary"
						onClick={() => router.push("/new-account")}
					>
						<Add fontSize="inherit" />
						<Typography fontSize={14}>Add account</Typography>
					</IconButton>
					<IconButton
						aria-label="add-account"
						size="large"
						color="primary"
						onClick={() => router.push("/new-transaction")}
					>
						<Typography fontSize={14}>Add transaction</Typography>
						<Add fontSize="inherit" />
					</IconButton>
				</Box>
			</Grid>
		</Container>
	);
}
