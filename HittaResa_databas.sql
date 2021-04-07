--Important--Create database (HittaResa) first!

CREATE TABLE [user] (
  [user_id] int PRIMARY KEY IDENTITY(1, 1),
  [email] nvarchar(50) UNIQUE,
  [username] nvarchar(50) UNIQUE,
  [password] varchar(MAX) CHECK(len([password])>=(8))
)
GO

CREATE TABLE [status] (
  [user_id] int,
  [image_id] int,
  [like_or_not] int,
  PRIMARY KEY ([user_id], [image_id])
)
GO

CREATE TABLE [images] (
  [image_id] int PRIMARY KEY IDENTITY(1, 1),
  [url] nvarchar(MAX) NOT NULL
)
GO

ALTER TABLE [status] ADD FOREIGN KEY ([user_id]) REFERENCES [user] ([user_id])
GO

ALTER TABLE [status] ADD FOREIGN KEY ([image_id]) REFERENCES [images] ([image_id])
GO

