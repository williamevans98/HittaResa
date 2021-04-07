--Important--Create database (HittaResa) first!

CREATE TABLE [user] (
  [user_id] int PRIMARY KEY IDENTITY(1, 1),
  [email] nvarchar(50) UNIQUE,
  [username] nvarchar(50) UNIQUE,
  [password] varchar(MAX) CHECK(len([password])>=(8))
)
GO

CREATE TABLE [has] (
  [like_or_not] int DEFAULT 0
)

GO

CREATE TABLE [images] (
  [image_id] int PRIMARY KEY IDENTITY(1, 1),
  [url] nvarchar(MAX) NOT NULL
)
GO

ALTER TABLE [has] ADD FOREIGN KEY ([like_or_not]) REFERENCES [user] ([user_id])
GO

ALTER TABLE [has] ADD FOREIGN KEY ([like_or_not]) REFERENCES [images] ([image_id])
GO

