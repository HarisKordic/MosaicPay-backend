import {
	Box,
	Container,
	Grid,
	Paper,
	SvgIcon,
	Typography,
} from "@mui/material";
import AccountInfoCard from "../../src/app/components/AccountInfoCard";
import { useRouter } from "next/navigation";
import { getUser, getUserAccounts } from "../../src/app/api";
import { useEffect, useState } from "react";
import AccountMenu from "../../src/app/components/AccountMenu";
import { TryRounded } from "@mui/icons-material";

export default function Home() {
	const router = useRouter();
	const [lastAccoundAdded, setLastAccountAdded] = useState(Object);
	const [username, setUsername] = useState("");

	let data;
	const getData = async () => {
		data = await getUserAccounts();
		const user = await getUser();
		setLastAccountAdded(data[data.length - 1]);
		setUsername(user.first_name);
	};
	useEffect(() => {
		getData();
	}, [data]);

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
				<Box
					sx={{
						width: "100%",
						mb: 3,
					}}
				>
					<Typography variant="h4" component={"h4"} fontWeight={"bold"}>
						Hello,{" "}
						{username?.substring(0, 1).toUpperCase() +
							username?.substring(1, username.length)}
					</Typography>
				</Box>
				<Box sx={{ mb: 5 }}>
					<AccountInfoCard
						balance={lastAccoundAdded?.balance}
						date={new Date().toDateString()}
						accountId={lastAccoundAdded.account_id}
						showDetail={true}
					></AccountInfoCard>
				</Box>
				<Box
					sx={{
						"& > :not(style)": {
							width: "100%",
						},
					}}
				>
					<Paper
						sx={{ height: "200px", width: "100%" }}
						elevation={15}
						variant="elevation"
						children={
							<Grid
								display={"flex"}
								flexDirection={"column"}
								width={"100%"}
								height={"100%"}
								justifyContent={"center"}
							>
								<Box width={"100%"} height={"100%"}></Box>
								<Box
									display={"flex"}
									flexDirection={"row"}
									justifyContent={"space-around"}
									onClick={() => router.push("/accounts-transactions")}
								>
									<SvgIcon color="secondary" sx={{ fontSize: 60 }}>
										<svg
											xmlns="http://www.w3.org/2000/svg"
											fill="none"
											viewBox="0 0 24 24"
											stroke-width="1.5"
											stroke="currentColor"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z"
											/>
										</svg>
									</SvgIcon>
									<SvgIcon color="secondary" sx={{ fontSize: 60 }}>
										<svg
											xmlns="http://www.w3.org/2000/svg"
											fill="none"
											viewBox="0 0 24 24"
											strokeWidth={1.5}
											stroke="currentColor"
										>
											<svg
												xmlns="http://www.w3.org/2000/svg"
												fill="none"
												viewBox="0 0 24 24"
												stroke-width="1.5"
												stroke="currentColor"
											>
												<path
													stroke-linecap="round"
													stroke-linejoin="round"
													d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z"
												/>
											</svg>
										</svg>
									</SvgIcon>
								</Box>

								<Box
									display={"flex"}
									flexDirection={"column"}
									justifyContent={"flex-end"}
									height={"100%"}
									sx={{ padding: "10px" }}
								>
									<Typography component={"p"} fontWeight={"bold"}>
										Accounts & Transactions
									</Typography>
								</Box>
							</Grid>
						}
					/>
				</Box>
			</Grid>
		</Container>
	);
}
